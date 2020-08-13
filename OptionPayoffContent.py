import dash_core_components as dcc
import dash_html_components as html

OPTION_PAYOFF_CONTENT = html.Div(children= [
        html.Div(className="topRow", children=[
        html.Div(className="row aboutRow", children=[
            html.H2("Option Strategy Payoff", className="aboutHeader"),
            html.P("This app is designed to provide you an easy way to visualize your payoff potential when engaging in various option strategies.  First,"
                   " you input the type of strategy you'd like to engage in, then you are prompted to input the necessary parameters of how you want to"
                   " engage in the strategy (i.e. if you would like to engage in a bull spread would you like to use call or put options).  Certain things worth noting is that number of contracts"
                   "is for each side of the arrangement so putting in 10 contracts for a Bull Call Spread would be selling 10 call contracts and buying 10 call contracts, for 20 total contracts."
                   "  Lastly, input the expected move as a positive percentage, for example, if the underlier is trading at $100/share and you are engaging in a Bear Put Spread, "
                   "then inputting a 5% move will assign your short put position a strike price of $95 and your long put position a strike price of $105."
                   " This application will provide a data table, coupled with a a graph, of how much you make or lose based on the level of the underlier at expiry "
                   "as well as maximum potential gain and loss. "),
            html.Strong(
                "*Note* This table and chart are very good approximations but not exact (a strike of 52.50 will show an underlier of 52 and 53 having the same payoff).  This is only a minute error, "
                "but it is worth noting.")
        ]),
        html.Div(className="row aboutRow optionPayoffInputRow", children=[
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
                        {'label': 'Straddle', 'value': 'straddle'},
                        {'label': 'Strangle', 'value': 'strangle'},
                        # {'label': 'Butterfly Spread', 'value': 'butterfly'}
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
        html.Div(id ="maxGainLossRow", className="row aboutRow"),
        html.Div(className="row aboutRow", children=[
            html.Div(id="optionPayoffTableWrapper")
        ]),
        html.Div(className="row aboutRow", children=[
            # TODO: Programmatically create payoff graph
            html.Div(id="optionPayoffGraphWrapper")
        ]),
    ]),
])