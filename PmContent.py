import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Sign
import pandas as pd
from companyStatScraper import getCurrMarketPrice, calcStockReturn

initDf = pd.DataFrame({"Ticker": [""], "No. Of Shares Held": [""], "$ Initially Invested Per Share": [""]})
initDf = initDf.reindex(sorted(initDf.columns, reverse=True), axis=1)

tickerList = initDf['Ticker'].values.tolist()
if tickerList == ['']:
    tickerList = []
oldPrice = initDf["$ Initially Invested Per Share"]
markPrice, betas = getCurrMarketPrice(tickerList)
ret = calcStockReturn(oldPrice, markPrice)
stockInfoInitDf = pd.DataFrame({"Ticker": tickerList, "Current Market Price": markPrice, "Return": ret, "Beta": betas})

PM_CONTENT = html.Div(children= [
    dcc.Store(id='local', storage_type='local'),
    html.Div(className="topRow", children=[
        html.Div(className="row aboutRow", children=[
            html.H2("Portfolio Management Tool", className="aboutHeader"),
            html.P("This app is designed to provide you with varying statistics based on the equities in your portfolio.  You may input the ticker "
                   "of any stock or ETF that may be in your portfolio, you then input the number of shares you have in that position and then finally "
                   "you must input the price per share at which the asset was purchased.  The app utilizes cookies to remember this information, so as long "
                   "as cookies are enabled and the browser is not on private browsing, your information will be stored.  If you would rather this not happen, or "
                   "prefer to keep cookies off or private browsing on, then the app will still work, you will just have to reinput your portfolio on every page "
                   "refresh. Things to keep in mind: "),
            html.Ul(className="tips", children=[
                html.Li("When you make a change on the page happen (addition or deletion of a row), the tab on your browser will say \"Updating\", do not make"
                        " any other changes until that goes away"),
                html.Li("If you accidentally do make multiple changes before waiting for an update I recommend doing a page refresh, it will be much more efficient "
                        "than letting the algorithm figure itself out"),
                html.Li("Do not have blank cells or rows, the bottom two tables only update when the input table is full"),
                html.Li("After you input a row, click onto a different cell within the table to trigger the event that updates the webpage"),
                html.Li("Occasionally Yahoo blocks our connection to their servers, if the first table is fully filled in, all tickers are real, the tab "
                        "doesn't say \"Updating\" and the last two tables are blank/don't update, try refreshing the page to fix the connection to Yahoo")
            ]),
            html.Strong("*Note* Generating the porftolio statistics table is extremely data intensive and involves a lot of computation, "
                        "if you add too many assets to your portfolio you may notice severe hangups in load time")
        ])
    ]),
    html.Div(className="tableWrapper row", children=[
        html.Div(id="positionInputTable", className="pmTable", children=[
            dash_table.DataTable(
                id='posTable',
                columns=[{"id": "Ticker", "name": "Ticker", "type": "text"},
                         {"id": "No. Of Shares Held", "name": "No. Of Shares Held", "type": "numeric"},
                         {"id": "$ Initially Invested Per Share", "name": "$ Initially Invested Per Share", "type": "numeric"}],
                style_header={
                    'backgroundColor': '#3399ff'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#b3d9ff'
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
                data=initDf.to_dict('records'),
                editable=True,
                row_deletable=True,
            ),
            html.Button("Add Row", id="addRowButton", className="btn-submit")
        ]),
    ]),
    html.Div(id="stockInfo", className="tableWrapper row", children=[
        html.Div(id="stockResultsTable", className="pmTableStock", children=[
            dash_table.DataTable(
                id='srTable',
                columns=[{"id": "Ticker", "name": "Ticker", "type": "text"},
                         {"id": "Current Market Price", "name": "Current Market Price", "type": "numeric"},
                         {"id": "% Of Portfolio", "name": "% Of Portfolio", "type": "numeric", 'format': FormatTemplate.percentage(2)},
                         {"id": "PnL", "name": "PnL", "type": "numeric"},
                         {"id": "Return", "name": "Return","type": "numeric", 'format': FormatTemplate.percentage(2).sign(Sign.positive)},
                         {"id": "Beta", "name": "Beta", "type": "numeric"},
                         {"id": "Standard Deviation", "name": "Standard Deviation", "type": "numeric", 'format': FormatTemplate.percentage(2)}],
                style_header={
                    'backgroundColor': '#3399ff'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px'
                },
                style_cell={'textAlign': 'center'},
                css=[{"selector": ".dash-spreadsheet", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'},
                     {"selector": ".dash-header", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'}],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#b3d9ff'
                    },
                    {
                        'if': {
                            'filter_query': '{PnL} > 0',
                            'column_id': 'PnL'
                        },
                        'color': '#33cc33'
                    },
                    {
                        'if': {
                            'filter_query': '{Return} > 0',
                            'column_id': 'Return'
                        },
                        'color': '#33cc33'
                    },
                    {
                        'if': {
                            'filter_query': '{PnL} < 0',
                            'column_id': 'PnL'
                        },
                        'color': '#ff704d'
                    },
                    {
                        'if': {
                            'filter_query': '{Return} < 0',
                            'column_id': 'Return'
                        },
                        'color': '#ff704d'
                    },
                ],
                data=stockInfoInitDf.to_dict('records'),
            ),
        ])
    ]),
    html.Div(id="pmInfo", className="tableWrapper row", children=[
        html.Div(id="pmResultTable", className="aboutRow", children=[
            dash_table.DataTable(
                id='pmTable',
                columns=[{"id": "Portfolio Return", "name": "Portfolio Return", "type": "numeric", 'format': FormatTemplate.percentage(2).sign(Sign.positive)},
                         {"id": "Portfolio PnL", "name": "Portfolio PnL", "type": "numeric"},
                         {"id": "Portfolio Beta", "name": "Portfolio Beta", "type": "numeric"},
                         {"id": "Portfolio Standard Deviation", "name": "Portfolio Standard Deviation", "type": "numeric", 'format': FormatTemplate.percentage(2)},
                         {"id": "Sharpe Ratio", "name": "Sharpe Ratio", "type": "numeric"},
                         {"id": "Treynor Ratio", "name": "Treynor Ratio", "type": "numeric"}],
                style_header={
                    'backgroundColor': '#3399ff'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px'
                },
                style_cell={'textAlign': 'center'},
                css=[{"selector": ".dash-spreadsheet", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'},
                     {"selector": ".dash-header", "rule": 'font-family: "Open Sans", verdana, arial, sans-serif'}],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#b3d9ff'
                    },
                    {
                        'if': {
                            'filter_query': '{Portfolio Return} > 0',
                            'column_id': 'Portfolio Return'
                        },
                        'color': '#33cc33',
                        'textWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{Portfolio Return} < 0',
                            'column_id': 'Portfolio Return'
                        },
                        'color': '#ff704d',
                        'textWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{Portfolio PnL} > 0',
                            'column_id': 'Portfolio PnL'
                        },
                        'color': '#33cc33',
                        'textWeight': 'bold'
                    },
                    {
                        'if': {
                            'filter_query': '{Portfolio PnL} < 0',
                            'column_id': 'Portfolio PnL'
                        },
                        'color': '#ff704d',
                        'textWeight': 'bold'
                    },
                ],
                data=[""],
                # export_format='xlsx',
                # export_headers='name',
            ),
        ])
    ]),
])