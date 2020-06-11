#################################
# IMPORTS
#################################
from datetime import datetime, timedelta
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import send_from_directory
import plotly.graph_objs as go
from datareader import *
import os
import pandas as pd
import numpy as np
from companyStatScraper import *
from EquityVisualizerContent import EQUITY_VISUALIZER_CONTENT
from AboutContent import ABOUT_CONTENT
from PmContent import PM_CONTENT

#################################
# INIT DASH AND FLASK
#################################
app = dash.Dash(__name__)
application = app.server


#################################
# CREATES APP LAYOUT - DATA GETS FILLED IN LATER
#################################
app.layout = html.Div(children= [
    dcc.Location(id='url', refresh=False),
    html.Div(className="banner", children=[
        html.Img(id='bannerImg'),
    ]),
    html.Div(className="navBar", children=[
        html.Ul(children=[
            dcc.Link(html.Li("Equity Visualization"), href="/", className="borderLi", refresh=True),
            dcc.Link(html.Li("Porfotlio Manager"), href="/pm", className="borderLi", refresh=True),
            dcc.Link(html.Li("About The Developer"), href="/about", refresh=True),
        ])
    ]),
    html.Div(id="content")
])


#################################
# SERVE CSS STYLESHEET
#################################
css_directory = os.getcwd() + '/assets/'
stylesheets = ['main.css']
static_css_route = '/assets/'
@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                stylesheet
            )
        )
    return send_from_directory(css_directory, stylesheet)
for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/assets/{}".format(stylesheet)})


#################################
# SERVE IMAGES
#################################
list_of_images = ['bannerEquity.png', 'banner404.png', 'bannerAbout.png', 'me.png', 'bannerPm.png']
@app.server.route('{}<image_path>.png'.format(static_css_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return send_from_directory(css_directory, image_name)
# app.index_string is how to modify the initial html


#################################
# SERVE WEBPAGE CONTENT / ROUTING
#################################
@app.callback(
    Output(component_id='content', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
)
def serveWebPage(pathname):
    if pathname == "/" or pathname == "":
        return EQUITY_VISUALIZER_CONTENT
    elif pathname == "/about":
        return ABOUT_CONTENT
    elif pathname == "/pm":
        return PM_CONTENT
    else:
        return ""


#################################
# SERVE CORRECT PAGE BANNER
#################################
@app.callback(
    Output(component_id='bannerImg', component_property='src'),
    [Input(component_id='url', component_property='pathname')]
)
def serveBanner(pathname):
    if pathname is None or pathname == "/" or pathname == "":
        return "/assets/bannerEquity.png"
    elif pathname == "/about":
        return "/assets/bannerAbout.png"
    elif pathname == "/pm":
        return "/assets/bannerPm.png"
    else:
        return "/assets/banner404.png"


#################################
# SAVE/USE PRE-COLLECTED DATA
#################################
toPickle = False
usePickle = False


##################################################################
# EQUITY VISUALIZATION CALLBACKS
##################################################################


#################################
# GENERATE STOCK GRAPH
#################################
@app.callback(
    Output(component_id="output-graph",component_property="children"),
    [Input(component_id="Symbolinput",component_property="value"),Input(component_id="StartInput",component_property="value")
     , Input(component_id="EndInput",component_property="value"), Input(component_id="bollinger",component_property="value")
     , Input(component_id="candleToggle", component_property="value")]
)
def update_value(input_data, start, end, bollinger, candle):
    global toPickle
    global usePickle
    # subtract 200 days from collection but dont graph it
    # Webscrapes date and close price based on ticker data
    origStart = start
    if usePickle:
        import pickle
        with open("./backupData/{0}/{0}-Company-Data".format(input_data), 'rb') as f:
            df = pickle.load(f)
            graphicalData = df.copy()
            f.close()
    else:
        if start is None or end is None or start == "":
            download_quotes(input_data,None,None)
        else:
            # print((datetime.strptime(start,"%Y-%m-%d") - BDay(200)))
            # start = int(time.mktime((datetime.strptime(start,"%Y-%m-%d") - BDay(200)).timetuple()))
            start = int(time.mktime((datetime.strptime(start, "%Y-%m-%d") - timedelta(days=300)).timetuple()))
            if end == "":
                end = int(time.mktime(datetime.strptime(datetime.strftime(datetime.today(),"%Y-%m-%d"),"%Y-%m-%d").timetuple()))
            else:
                end = int(time.mktime(datetime.strptime(end,"%Y-%m-%d").timetuple()))
            download_quotes(input_data,start,end)
        df = pd.read_csv(input_data + ".csv")
        if origStart is not None and origStart != "":
            graphicalData = df[pd.to_datetime(df.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = df.copy()
        # graphicalData.reset_index(inplace=True, drop=True)
        os.remove(input_data + ".csv")
    if toPickle:
        import pickle
        if not os.path.exists("backupData/{0}".format(input_data)):
            os.mkdir("backupData/{0}".format(input_data))
        with open("./backupData/{0}/{0}-Company-Data".format(input_data), 'wb') as f:
            pickle.dump(df, f)
            f.close()
    # meanCalc = df.copy(deep=True)
    if bollinger is None:
        bollinger = []
    df.set_index('Date', inplace=True)
    df.replace("null", np.nan, inplace=True)
    df.dropna(inplace=True)
    df.astype(float)
    graphicalData = df[df.index >= origStart]
    #Make first bar green
    color = ['rgb(0,255,0)']
    closeList = df.Close.values.tolist()
    for i in range(len(closeList)):
        if i > 0:
            if closeList[i] < closeList[i-1]:
                color += ['rgb(255,0,0)']
            else:
                color += ['rgb(0,255,0)']
    volColor = []
    for i in range(len(closeList)):
        volColor += ['rgb(0,0,255)']
    layout = {
        'title': input_data
    }
    data = []
    volData = []
    volData += [{'x': graphicalData.index, 'y': graphicalData.Volume,'type':'bar','marker':dict(color=color), 'name': "Volume"}]
    if candle:
        trace = go.Candlestick(x=graphicalData.index,
                               open=graphicalData.Open,
                               high=graphicalData.High,
                               low=graphicalData.Low,
                               close=graphicalData.Close,name=input_data)
        layout = go.Layout(
            title=input_data,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )
        data += [trace]
    else:
        data += [{'x': graphicalData.index, 'y': graphicalData.Close, 'type': 'line', 'name': input_data}]

    if "check" in bollinger:
        # avg = meanCalc.rolling(window=20).mean()
        # std = meanCalc.rolling(window=20).std()
        avg = df.rolling(window=20).mean()
        std = df.rolling(window=20).std()
        df['Upper'] = avg['Close'] + (std['Close']*2)
        df['Middle'] = avg['Close']
        df['Lower'] = avg['Close'] - (std['Close']*2)
        high = []
        middle= []
        low = []
        for i in range(len(closeList)):
            high += ['rgb(0,255,0)']
            middle+=['rgb(0,0,255)']
            low += ['rgb(255,0,0)']
        if origStart is not None and origStart != "":
            graphicalData = df[pd.to_datetime(df.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = df.copy()
        data += [{'x' : graphicalData.index, 'y': graphicalData.Upper,'type':'line','marker':dict(color=high),'name':'Upper Bollinger Band'},
                    {'x' : graphicalData.index, 'y': graphicalData.Middle,'type':'line','marker':dict(color=middle),'name':'Middle Bollinger Band'},
                    {'x' : graphicalData.index, 'y': graphicalData.Lower,'type':'line','marker':dict(color=low),'name':'Lower Bollinger Band'}]
    if "200SMA" in bollinger:
        roll = df.rolling(window=200).mean()
        if origStart is not None and origStart != "":
            graphicalData = roll[pd.to_datetime(roll.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = roll
        data += [{'x': graphicalData.index, 'y': graphicalData['Close'],'type':'line', 'name': '200 Day MA'}]
        volData += [{'x': graphicalData.index, 'y': graphicalData['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '200 Day MA'}]
    if "150SMA" in bollinger:
        roll = df.rolling(window=150).mean()
        if origStart is not None and origStart != "":
            graphicalData = roll[pd.to_datetime(roll.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = roll
        data += [{'x': graphicalData.index, 'y': graphicalData['Close'],'type':'line', 'name': '150 Day MA'}]
        volData += [{'x': graphicalData.index, 'y': graphicalData['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '150 Day MA'}]
    if "100SMA" in bollinger:
        roll = df.rolling(window=100).mean()
        if origStart is not None and origStart != "":
            graphicalData = roll[pd.to_datetime(roll.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = roll
        data += [{'x': graphicalData.index, 'y': graphicalData['Close'],'type':'line', 'name': '100 Day MA'}]
        volData += [{'x': graphicalData.index, 'y': graphicalData['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '100 Day MA'}]
    if "50SMA" in bollinger:
        roll = df.rolling(window=50).mean()
        if origStart is not None and origStart != "":
            graphicalData = roll[pd.to_datetime(roll.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = roll
        data += [{'x': graphicalData.index, 'y': graphicalData['Close'],'type':'line', 'name': '50 Day MA'}]
        volData += [{'x': graphicalData.index, 'y': graphicalData['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '50 Day MA'}]
    if "50EWMA" in bollinger:
        roll = df.ewm(span=50, min_periods=50).mean()
        if origStart is not None and origStart != "":
            graphicalData = roll[pd.to_datetime(roll.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = roll
        data += [{'x': graphicalData.index, 'y': graphicalData['Close'],'type':'line', 'name': '50 Day EWMA'}]
        volData += [{'x': graphicalData.index, 'y': graphicalData['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '50 Day EWMA'}]
    if "20EWMA" in bollinger:
        roll = df.ewm(span=20, min_periods=20).mean()
        if origStart is not None and origStart != "":
            graphicalData = roll[pd.to_datetime(roll.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = roll
        data += [{'x': graphicalData.index, 'y': graphicalData['Close'],'type':'line', 'name': '20 Day EWMA'}]
        volData += [{'x': graphicalData.index, 'y': graphicalData['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '20 Day EWMA'}]
    if '14SRSI' in bollinger:
        # https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas#29400434
        close = df['Close']
        delta = close.diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up2 = up.rolling(14).mean()
        roll_down2 = down.abs().rolling(14).mean()
        rs = roll_up2 / roll_down2
        rsi = 100.0 - (100.0 / (1.0 + rs))
        df['14SRSI'] = rsi
        if origStart is not None and origStart != "":
            graphicalData = df[pd.to_datetime(df.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = df.copy()
        data += [{'x': graphicalData.index, 'y': graphicalData['14SRSI'], 'type': 'line', 'name': '14 Day RSI (SMA)'}]
    if '14ERSI' in bollinger:
        close = df['Close']
        delta = close.diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up1 = up.ewm(span=14).mean()
        roll_down1 = down.abs().ewm(span=14).mean()
        # Calculate the RSI based on EWMA
        rs = roll_up1 / roll_down1
        rsi = 100.0 - (100.0 / (1.0 + rs))
        df['14ERSI'] = rsi
        if origStart is not None and origStart != "":
            graphicalData = df[pd.to_datetime(df.index, format="%Y-%m-%d") >= datetime.strptime(origStart, "%Y-%m-%d")]
        else:
            graphicalData = df.copy()
        data += [{'x': graphicalData.index, 'y': graphicalData['14ERSI'], 'type': 'line', 'name': '14 Day RSI (EWMA)'}]
    header = html.H2(input_data, className="graphHead title")
    return [header, dcc.Graph(
            id='example_graph',
            figure= {
                'data':data,
                # 'layout': layout
            }
        ),
        dcc.Graph(
            id='volume',
            style={"height":"300px"},
            figure= {
                'data' : volData
            }
        )
        ]


#################################
# GENERATE OWNERSHIP PIE CHART
#################################
@app.callback(
    Output(component_id="ownership-pie", component_property="children"),
    [Input(component_id="Symbolinput", component_property="value")]
)
def shareOwnershipChart(ticker):
    try:
        getData = companyStatScraper.getInstiutionalOwnership(ticker)
        # Use pull to make a certain one separate
        # trace = go.Pie(labels = list(getData.keys()), values = list(getData.values()), pull=[0.2, 0.2, 0.2], hole=.4, hoverinfo="label+percent")
        trace = go.Pie(labels=list(getData.keys()), values=list(getData.values()), hole=.4, hoverinfo="label+percent")
        # layout = go.Layout(
        #     title = "Institutional Ownership"
        # )
        data = [trace]
        header = html.H2("Institutional Ownership", className="graphHead")
        return [header, dcc.Graph(
                id='ownership',
                style={"height":"550px"},
                figure= {
                    'data':data,
                    # 'layout': layout
                }
            )]
    except:
        # TODO: Some kind of div saying that ownership info only available for stocks not ETFs or overall market
        return ""


#################################
# GENERATE SHORT SELLING DATA TABLE
#################################
@app.callback(
    Output(component_id="shortTable", component_property="children"),
    [Input(component_id="Symbolinput", component_property="value")]
)
def shortShareTable(ticker):
    try:
        getData = companyStatScraper.getShortShares(ticker)
        dataDf = pd.DataFrame({"1": getData[0], "2": getData[1]})
        header = html.H2("Short Position Information", className="graphHead")
        table = dash_table.DataTable(
            id='shortTableInner',
            columns=[{"name": i, "id": i} for i in dataDf.columns],
            data= dataDf.to_dict('records'),
            style_header={
                'display': 'none'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#3399ff'
                }
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={'textAlign': 'center'},
            css=[{"selector": ".dash-spreadsheet", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'}],
        )
        return [header,table]
    except:
        # TODO: Some kind of div saying that ownership info only available for stocks not ETFs or overall market
        return ""


#################################
# GENERATE EARNINGS BAR CHART
#################################
@app.callback(
    Output(component_id="earnings-graph", component_property="children"),
    [Input(component_id="Symbolinput", component_property="value")]
)
def earningsChart(ticker):
    try:
        getData = companyStatScraper.getEarningsHist(ticker)
        data = [
            {"x": getData[0], "y": getData[1], 'type': 'bar', 'name': 'EPS Est.'},
            {"x": getData[0], "y": getData[2], 'type': 'bar', 'name': 'EPS Act.'},
        ]
        header = html.H2("Earnings History", className="graphHead")
        return [header, dcc.Graph(
                id='earnings',
                # style={"height":"650px"},
                figure= {
                    'data': data,
                },
                style={
                    'height': 550,
                    # 'width': 1200,
                },
            )]
    except:
        # TODO: Some kind of div saying that ownership info only available for stocks not ETFs or overall market
        return ""


#################################
# GENERATE COMPANY BIO
#################################
@app.callback(
    Output(component_id="company-bio", component_property="children"),
    [Input(component_id="Symbolinput", component_property="value")]
)
def companyBio(ticker):
    try:
        getData = companyStatScraper.getCompanyBio(ticker)
        header = html.H2("About {0}".format(ticker), className="graphHead snap")
        return [header, html.P(getData, className="bio")]
    except:
        # TODO: Some kind of div saying that ownership info only available for stocks not ETFs or overall market
        return ""


#################################
# GENERATE TOP INSTITUTIONAL OWNERSHIP TABLE
#################################
@app.callback(
    Output(component_id="top-institutional", component_property="children"),
    [Input(component_id="Symbolinput", component_property="value")]
)
def topInstitutional(ticker):
    try:
        getData = companyStatScraper.getFundOwnership(ticker)[0]
        header = html.H2("Top Institutional Owners", className="graphHead title")
        table = dash_table.DataTable(
            id='instTable',
            columns=[{"name": i, "id": i} for i in getData.columns],
            data= getData.to_dict('records'),
            style_as_list_view=True,
            style_header={
                # 'display': 'none'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#3399ff'
                }
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={'textAlign': 'center'},
            css=[{"selector": ".dash-spreadsheet", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'},
                 {"selector": ".dash-header", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'}],
        )
        return [header, table]
    except:
        # TODO: Some kind of div saying that ownership info only available for stocks not ETFs or overall market
        return ""


#################################
# GENERATE TOP MUTUAL FUND OWNERSHIP TABLE
#################################
@app.callback(
    Output(component_id="top-mutual", component_property="children"),
    [Input(component_id="Symbolinput", component_property="value")]
)
def topMutual(ticker):
    try:
        getData = companyStatScraper.getFundOwnership(ticker)[1]
        header = html.H2("Top Mutual Fund Owners", className="graphHead title")
        table = dash_table.DataTable(
            id='instTable',
            columns=[{"name": i, "id": i} for i in getData.columns],
            data= getData.to_dict('records'),
            style_as_list_view=True,
            style_header={
                # 'display': 'none'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#3399ff'
                }
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={'textAlign': 'center'},
            css=[{"selector": ".dash-spreadsheet", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'},
                 {"selector": ".dash-header", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'}],
        )
        return [header,table]
    except:
        # TODO: Some kind of div saying that ownership info only available for stocks not ETFs or overall market
        return ""


##################################################################
# ABOUT ME CALLBACKS
##################################################################



##################################################################
# PORTFOLIO MANAGEMENT CALLBACKS
##################################################################


#################################
# ADD ROWS TO DATATABLE
#################################
testClicks = 0
@app.callback(Output('posTable', 'data'),
              [Input("local", 'modified_timestamp'), Input('addRowButton', 'n_clicks')],
              [State('posTable', 'data'), State("local", "data")]
)
def addRowToPm(timestamp, n_clicks, posData, localData):
    global testClicks
    if len(posData) == 0:
        df = pd.DataFrame({"Ticker": [""], "No. Of Shares Held": [""], "$ Initially Invested Per Share": [""]})
    elif posData[0]['Ticker'] == '' and posData[0]['No. Of Shares Held'] == '' and posData[0]['$ Initially Invested Per Share'] == '' and len(posData) == 1:
        df = pd.read_json(localData, orient='split')
        if df.empty:
            df = pd.DataFrame({"Ticker": [""], "No. Of Shares Held": [""], "$ Initially Invested Per Share": [""]})
    else:
        df = pd.DataFrame(posData)
    if n_clicks is not None and n_clicks > 0:
        testClicks += 1
        if testClicks == n_clicks:
            df = df.append({"Ticker": "", "No. Of Shares Held": "", "$ Initially Invested Per Share": ""}, ignore_index=True)
        else:
            testClicks -= 1
    return df.to_dict('records')


#################################
# MODIFY ROW FROM STOCK TABLE ON INPUT TABLE DELETION OR ADDITION
#################################
@app.callback(Output('srTable', 'data'),
              [Input('posTable', 'data')],
              [State('srTable', 'data')]
)
def modifyStockRow(inputData, stockData):
    inpDf = pd.DataFrame(inputData)
    listData = inpDf.values.flatten()
    # Differentiate between one stock with blank values and lots of stocks where only one has blank values
    if len(listData) == 3 and '' in listData:
        return []
    if '' in listData:
        return stockData
    else:
        sDf = pd.DataFrame(stockData)
        inpTickers = inpDf['Ticker'].values.tolist()
        if sDf.empty:
            stockTickers = []
        else:
            stockTickers = sDf['Ticker'].values.tolist()
        if len(inpTickers) > len(stockTickers):
            if len(stockTickers) == 0:
                toAdd = inpDf
            else:
                toAdd = inpDf[~inpDf['Ticker'].isin(sDf['Ticker'].values.tolist())]
            tickerList = toAdd['Ticker'].values.tolist()
            oldPrice = toAdd["$ Initially Invested Per Share"]
            markPrice = getCurrMarketPrice(tickerList)
            ret = calcStockReturn(oldPrice.values.tolist(), markPrice)
            stockInfoDf = pd.DataFrame({"Ticker": tickerList, "Current Market Price": markPrice, "Return": ret})
            if sDf.empty:
                sDf = stockInfoDf
            else:
                sDf = sDf.append(stockInfoDf)
        else:
            oldPrice = inpDf["$ Initially Invested Per Share"]
            markPrice = getCurrMarketPrice(inpTickers)
            ret = calcStockReturn(oldPrice.values.tolist(), markPrice)
            sDf = pd.DataFrame({"Ticker": inpTickers, "Current Market Price": markPrice, "Return": ret})
        return sDf.to_dict('records')


#################################
# FIX PORTFOLIO RETURN AFTER ADDED OR DELETED STOCK
#################################
@app.callback(Output('pmTable', 'data'),
              [Input('srTable', 'data')],
              [State('posTable', 'data'), State('pmTable', 'data')]
)
def fixPMReturn(stockData, inputData, portData):
    inpDf = pd.DataFrame(inputData)
    listData = inpDf.values.flatten()
    if len(listData) == 3 and '' in listData:
        return []
    if '' in listData:
        return portData
    else:
        sDf = pd.DataFrame(stockData)
        newRet = calcPortReturn(inpDf['$ Initially Invested Per Share'].astype(float).values.tolist(), sDf['Current Market Price'].astype(float).values.tolist(),
                       inpDf['No. Of Shares Held'].astype(float).values.tolist())
        newRetDf = pd.DataFrame({'Return': [newRet]})
        return newRetDf.to_dict('records')


#################################
# STORE STOCK SELECTIONS SO YOU DONT HAVE TO INPUT IT EVERY TIME
#################################
@app.callback(
    Output('local', 'data'),
    [Input("posTable", "data")]
)
def storeSession(inputData):
    df = pd.DataFrame(inputData)
    return df.to_json(orient="split")


##################################################################
# RUN APPLICATION
##################################################################
if __name__ == '__main__':
    # For deployment
    # application.run(debug=True, host='0.0.0.0', port='80')
    # For local
    application.run(debug=False)