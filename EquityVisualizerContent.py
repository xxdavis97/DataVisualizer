import dash_core_components as dcc
import dash_html_components as html


EQUITY_VISUALIZER_CONTENT = html.Div(children= [
    html.Div(
        className="headerBox",
        children=[
            html.Div(
                className = "searchParameterContainer",
                children= [
                    html.Div(children="Input ticker: "),
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
        html.Div(id="options", className="six columns owner"),
        # html.Div(id="top-mutual", className="six columns owner"),

    ], className="row bottomRow"),
])