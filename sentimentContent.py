import dash_core_components as dcc
import dash_html_components as html
import twitterSentiment
import nltk

# try:
#     nltk.download('punkt')
# except Exception as e:
#     from logger import logError
#     logError(e, "NLTK TOKEN")
twitterSentiment.runStream()
SENTIMENT_CONTENT = html.Div(children= [
    html.Div(children = [
        html.Div(className="topRow", children = [
            html.Div(className="row aboutRow", children=[
                html.H2("Twitter Sentiment Analysis", className="aboutHeader"),
                html.P(
                    "The graph below is a plot of how users on Twitter feel about the current state of the markets.  The algorithm gathers any Tweet that contains the key words: S&P 500, S&P, Dow, Dow Jones, DJI, "
                    "Standard And Poors, Nasdaq, FANG, QQQ, or Stock.  These tweets are collected live, and put through a Natural Language Processing (NLP) algorithm to determine whether "
                    "the overall sentiment of the tweet is positive or negative.  The sentiment quotient (y-axis) gets a 1 added as positive tweets filter in and a 1 subtracted as negative tweets filter in.  Thus,"
                    " if the graph is currently hovering over a largely negative or largely positive number, that means the twitter feed is overall pessimistic or optimistic respectively.  The x-axis "
                    "is relatively insignifcant, just showing the tweet number of the latest 300 tweets collected."),
            ]),
        ]),
        html.Div(className="row aboutRow", children=[
            dcc.Graph(id='sentiment-graph'),
            dcc.Interval(
                id='sentiment-interval',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ])
    ])
])
