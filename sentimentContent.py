import dash_core_components as dcc
import dash_html_components as html
import twitterSentiment
import nltk

twitterSentiment.runStream()
SENTIMENT_CONTENT = html.Div(children= [
    html.Div(children = [
        html.Div(className="topRow", children = [
            html.Div(className="row aboutRow", children=[
                html.H2("Twitter Sentiment Analysis", className="aboutHeader"),
                html.P(
                    "The graph below is a plot of how users on Twitter feel about the current state of the markets.  The x-axis is relatively insignificant"
                    ", it only states how sentiment moves over the course of the latest 300 tweets the algorithm collected.  The y-axis is what's important.  "
                    "The algorithm gathers any Tweet that contains the key words: S&P 500, S&P, Dow, Dow Jones, DJI, Standard And Poors, Nasdaq, "
                    "FANG, QQQ, or Stock.  These tweets are collected live and put through a Natural Language Processing alogrithm to determine whether "
                    "the overall sentiment of the tweet is good or bad.  The y-axis gets a 1 added to it when the tweet is positive, and a 1 subtracted to "
                    "it when the tweet is positive.  "),
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
