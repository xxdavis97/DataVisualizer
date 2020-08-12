import dash_core_components as dcc
import dash_html_components as html

OPTION_PAYOFF_CONTENT = html.Div(children= [
        html.Div(className="topRow", children=[
        html.Div(className="row aboutRow", children=[
            html.H2("Option Strategy Payoff", className="aboutHeader"),
            html.P("This app is designed to provide you an easy way to visualize your payoff potential when engaging in various option strategies.  First,"
                   " you input the type of strategy you'd like to engage in, then you are prompted to input the necessary parameters of how you want to"
                   " engage in the strategy (i.e. if you would like to engage in a bull spread would you like to use call or put options).  You will"
                   " also of course need to input the underlier as well as the expiration date of the options and the number of contracts you'd like each (i.e. if you're doing a bull spread"
                   "and put 10 contracts that means 10 short contracts and 10 long contracts.  Lastly, input the expected move as a positive percentage,"
                   " for example, if the underlier is trading at $100/share and you are engaging in a Bear Put Spread, then inputting a 5% move will assign your short put position a"
                   " strike price of $95 and your long put position a strike price of $105."
                   " This application will provide a data table, coupled with a a graph, of how much you make or lose per differing movements in the underlier "
                   "as well as maximum potential gain and loss. "),
        ]),
        html.Div(className="row aboutRow", children=[
            html.Div(className="six columns", children=[
                html.Label(className="optionStratLabel", htmlFor="Symbolinput", children="Ticker: "),
                dcc.Input(id="Symbolinput", value="", type="text"),
                html.Label(className="optionStratLabel", htmlFor="expiryDate", children="Expiry: "),
                dcc.Input(id="expiryDate", value="", type="date"),
                html.Label(className="numContractLabel", htmlFor="numContract", children="Number Of Contracts: "),
                dcc.Input(id="numContract", value="", type="text"),
                dcc.Dropdown(
                    className="optionStratDrop",
                    # TODO: Straddle, Strangle, Butterfly
                    options=[
                        {'label': 'Bull Spread', 'value': 'bull'},
                        {'label': 'Bear Spread', 'value': 'bear'},
                    ],
                    id='optionStrat',
                    searchable=False,
                    placeholder="Option Strategy"
                ),
                dcc.Dropdown(
                    className="optionStratDrop",
                    options=[
                        {'label': 'Call', 'value': 'call'},
                        {'label': 'Put', 'value': 'put'},
                    ],
                    id='optionType',
                    searchable=False,
                    placeholder="Option Type"
                ),
                html.Label(className="optionStratLabel", htmlFor="percMove", children="Expected Move (%): "),
                dcc.Input(id="percMove", value="", type="text"),
                html.Button("Calculate", id="calcPayoffButton", className="btn-submit")
            ]),
        ]),
        html.Div(className="row aboutRow", children=[
            # TODO: Programmatically fill in max loss and max gain also only show these after you hit submit
            html.Div(className="six columns readOnlyDivWrap", children=[
                html.Label(className="optionStratLabel", htmlFor="maxLoss", children="Maximum Loss: "),
                dcc.Input(id="maxLoss", className="readOnlyInput", value="", type="text", readOnly=True)
            ]),
            html.Div(className="six columns readOnlyDivWrap", children=[
                html.Label(className="optionStratLabel", htmlFor="maxGain", children="Maximum Gain  : "),
                dcc.Input(id="maxGain", className="readOnlyInput", value="", type="text", readOnly=True)
            ])
        ]),
        html.Div(className="row aboutRow", children=[
            # TODO: Programmatically fill in table like i do in excel
            html.Div(id="optionPayoffTableWrapper")
        ]),
        html.Div(className="row aboutRow", children=[
            # TODO: Programmatically create payoff graph
            html.Div(id="optionPayoffGraphWrapper")
        ]),
    ]),
])