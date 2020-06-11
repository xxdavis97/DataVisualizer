import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Sign
import pandas as pd
from companyStatScraper import getCurrMarketPrice, calcStockReturn, calcPortReturn

initDf = pd.DataFrame({"Ticker": [""], "No. Of Shares Held": [""], "$ Initially Invested Per Share": [""]})
initDf = initDf.reindex(sorted(initDf.columns, reverse=True), axis=1)

# TODO: Implied Vol
tickerList = initDf['Ticker'].values.tolist()
if tickerList == ['']:
    tickerList = []
oldPrice = initDf["$ Initially Invested Per Share"]
markPrice = getCurrMarketPrice(tickerList)
ret = calcStockReturn(oldPrice, markPrice)
stockInfoInitDf = pd.DataFrame({"Ticker": tickerList, "Current Market Price": markPrice, "Return": ret})

PM_CONTENT = html.Div(children= [
    dcc.Store(id='local', storage_type='local'),
    html.Div(className="pmHowTo", children=[
        html.Div(className="row aboutRow", children=[
            html.H2("Portfolio Management Tool", className="aboutHeader"),
            html.P("This app is designed to provide you with varying statistics based on the equities in your portfolio.  You may input the ticker "
                   "of any stock or ETF that may be in your portfolio, you then input the number of shares you have in that position and then finally "
                   "you must input the price per share at which the asset was purchased.  The app utilizes cookies to remember this information, so as long "
                   "as cookies are enabled and the browser is not on private browsing, your information will be stored.  If you would rather this not happen, or "
                   "prefer to keep cookies off or private browsing on, then the app will still work, you will just have to reinput your portfolio on every page "
                   "refresh. ")
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
                data=initDf.to_dict('records'),
                editable=True,
                row_deletable=True,
            ),
            html.Button("Add Row", id="addRowButton", className="btn-submit")
        ]),
    ]),
    html.Div(id="stockInfo", className="tableWrapper row", children=[
        html.Div(id="stockResultsTable", className="pmTable", children=[
            dash_table.DataTable(
                id='srTable',
                columns=[{"id": "Ticker", "name": "Ticker", "type": "text"},
                         {"id": "Current Market Price", "name": "Current Market Price", "type": "numeric"},
                         {"id": "Return", "name": "Return","type": "numeric", 'format': FormatTemplate.percentage(2).sign(Sign.positive)}],
                style_header={
                    'backgroundColor': '#3399ff'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#b3d9ff'
                    }
                ],
                data=stockInfoInitDf.to_dict('records'),
            ),
        ])
    ]),
    html.Div(id="pmInfo", className="tableWrapper row", children=[
        html.Div(id="pmResultTable", className="pmTable", children=[
            # TODO: Beta
            dash_table.DataTable(
                id='pmTable',
                columns=[{"id": "Return", "name": "Return", "type": "numeric", 'format': FormatTemplate.percentage(2).sign(Sign.positive)}],
                style_header={
                    'backgroundColor': '#3399ff'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#b3d9ff'
                    }
                ],
                data=[""],
            ),
        ])
    ]),
])