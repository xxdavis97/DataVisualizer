from datetime import datetime, timedelta
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import send_from_directory
import plotly.graph_objs as go
from datareader import *
import os
import pandas as pd
import numpy as np
import companyStatScraper

app = dash.Dash(__name__)


# CSS Setup
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css',
# })
css_directory = os.getcwd() + '/assets/'
stylesheets = ['main.css']
list_of_images = ['Header.png', 'banner.png']
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

@app.server.route('{}<image_path>.png'.format(static_css_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return send_from_directory(css_directory, image_name)
# app.index_string is how to modify the initial html


# Creates the layout of an input field and an empty div that will hold the graph
app.layout = html.Div(children= [
    html.Div(className="banner", children = [
        html.Img(src='/assets/banner.png'),
    ]),
    html.Div(
        className="headerBox",
        children=[
            html.Div(
                className = "searchParameterContainer",
                children= [
                    html.Div(children="Symbol to graph: "),
                    # Change default back to SPY
                    dcc.Input(id="Symbolinput",value="SNAP",type="text"),
                    # html.Button(id="newStock"),
                    dcc.Input(id="StartInput",value="",type="date"),
                    dcc.Input(id="EndInput",value="",type="date"),
                    dcc.RadioItems(
                        className="candleToggle",
                        options = [
                            {'label': 'Price Plot', 'value': False},
                            {'label': 'Candlestick Plot', 'value': True}],
                        id = "candleToggle",
                        value= False
                    ),
                    dcc.Dropdown(
                        className= "optionDrop",
                        options = [
                            # {'label': 'Price', 'value': 'price'},
                            {'label': 'Bollinger Bands', 'value': 'check'},
                            # {'label': 'Candlestick', 'value': 'candle'},
                            {'label': '200 Day SMA', 'value': '200SMA'},
                            {'label': '150 Day SMA', 'value': '150SMA'},
                            {'label': '100 Day SMA', 'value': '100SMA'},
                            {'label': '50 Day SMA', 'value': '50SMA'},
                            {'label': '50 Day EWMA', 'value': '50EWMA'},
                            {'label': '20 Day EWMA', 'value': '20EWMA'},
                            {'label': '14 Day RSI (SMA)', 'value': '14SRSI'},
                            {'label': '14 Day RSI (EWMA)', 'value': '14ERSI'},
                        ],
                        id = 'bollinger',
                        # value = ["price"],
                        multi=True,
                        searchable=False,
                        placeholder="More options"
                    )
            ])
    ]),
    html.Div(id="output-graph"),
    html.Div(id="twoGraphCol", children = [
        html.Div(id="company-bio", className="six columns"),
        html.Div(id="earnings-graph", className="six columns"),

    ], className="row"),
    html.Div(id="earningsAndAbout", children = [
        html.Div(id="ownership-pie", className="six columns"),
        html.Div(id="shortTable", className="six columns"),

    ], className="row"),
    html.Div(id="fundOwnership", children=[
        html.Div(id="top-institutional", className="six columns owner"),
        html.Div(id="top-mutual", className="six columns owner"),

    ], className="row"),
])

toPickle = False
usePickle = False
# Our callback function that runs every time input field changes
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
    if usePickle:
        import pickle
        with open("./backupData/{0}/{0}-Company-Data".format(input_data), 'rb') as f:
            df = pickle.load(f)
            f.close()
    else:
        if start is None or end is None or start == "":
            download_quotes(input_data,None,None)
        else:
            # print((datetime.strptime(start,"%Y-%m-%d") - BDay(200)))
            # start = int(time.mktime((datetime.strptime(start,"%Y-%m-%d") - BDay(200)).timetuple()))
            start = int(time.mktime((datetime.strptime(start, "%Y-%m-%d")).timetuple()))
            if end == "":
                end = int(time.mktime(datetime.strptime(datetime.strftime(datetime.today(),"%Y-%m-%d"),"%Y-%m-%d").timetuple()))
            else:
                end = int(time.mktime(datetime.strptime(end,"%Y-%m-%d").timetuple()))
            download_quotes(input_data,start,end)
        df = pd.read_csv(input_data+ ".csv")
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
    # print(df.index[0:199])
    # df = df.iloc[200:]
    # print(df)
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
    volData += [{'x': df.index, 'y': df.Volume,'type':'bar','marker':dict(color=color), 'name': "Volume"}]
    if candle:
        trace = go.Candlestick(x=df.index,
                               open=df.Open,
                               high=df.High,
                               low=df.Low,
                               close=df.Close,name=input_data)
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
        data += [{'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data}]

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
        data += [{'x' : df.index, 'y': df.Upper,'type':'line','marker':dict(color=high),'name':'Upper Bollinger Band'},
                    {'x' : df.index, 'y': df.Middle,'type':'line','marker':dict(color=middle),'name':'Middle Bollinger Band'},
                    {'x' : df.index, 'y': df.Lower,'type':'line','marker':dict(color=low),'name':'Lower Bollinger Band'}]
    if "200SMA" in bollinger:
        data += [{'x': df.index, 'y': df.rolling(window=200).mean()['Close'],'type':'line', 'name': '200 Day MA'}]
        volData += [{'x': df.index, 'y': df.rolling(window=200).mean()['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '200 Day MA'}]
    if "150SMA" in bollinger:
        data += [{'x': df.index, 'y': df.rolling(window=150).mean()['Close'],'type':'line', 'name': '150 Day MA'}]
        volData += [{'x': df.index, 'y': df.rolling(window=150).mean()['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '150 Day MA'}]
    if "100SMA" in bollinger:
        data += [{'x': df.index, 'y': df.rolling(window=100).mean()['Close'],'type':'line', 'name': '100 Day MA'}]
        volData += [{'x': df.index, 'y': df.rolling(window=100).mean()['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '100 Day MA'}]
    if "50SMA" in bollinger:
        data += [{'x': df.index, 'y': df.rolling(window=50).mean()['Close'],'type':'line', 'name': '50 Day MA'}]
        volData += [{'x': df.index, 'y': df.rolling(window=50).mean()['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '50 Day MA'}]
    if "50EWMA" in bollinger:
        data += [{'x': df.index, 'y': pd.ewma(df, span=50, min_periods=50)['Close'],'type':'line', 'name': '50 Day EWMA'}]
        volData += [{'x': df.index, 'y': pd.ewma(df, span=50, min_periods=50)['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '50 Day EWMA'}]
    if "20EWMA" in bollinger:
        data += [{'x': df.index, 'y': pd.ewma(df, span=20, min_periods=20)['Close'],'type':'line', 'name': '20 Day EWMA'}]
        volData += [{'x': df.index, 'y': pd.ewma(df, span=20, min_periods=20)['Volume'], 'type': 'line','marker':dict(color=volColor), 'name': '20 Day EWMA'}]
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
        data += [{'x': df.index, 'y': rsi, 'type': 'line', 'name': '14 Day RSI (SMA)'}]
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
        data += [{'x': df.index, 'y': rsi, 'type': 'line', 'name': '14 Day RSI (EWMA)'}]
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

if __name__ == "__main__":
    app.run_server(debug=False)