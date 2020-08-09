from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sentiment_mod as s
import json
from logger import logTwitterError, logTweets, logError
# TODO: Add tweepy, scipy, and nltk to requirements.txt

consumer_key = "rdhYkY62dMnwclSGNUDfK44r4"
consumer_secret = "H2tH8OLcb7j5tjFrRJNTyxZilzgoKE2OlQzaXfGeyYm1LMvdEc"
access_token = "1044066351638286336-Mvif5sOzBnS2JEDjaoByH8rlvAKMaX"
access_secret = "Aw4QERisoqoj2kIAIrCugfObDUPyHp1DTPUxr1kzWeDSl"

testList = []

class listener(StreamListener):
    def on_data(self, data):
        global testList
        all_data = json.loads(data)
        tweet = all_data["text"]
        try:
            sentiment_value, confidence =s.sentiment(tweet)
            logTweets(sentiment_value)
        except Exception as e:
            logError(e, "Listener")
        # print(tweet, sentiment_value, confidence)
        sentiment_value, confidence = s.sentiment(tweet)
        if confidence * 100 >= 80:
            output = open("twitter-out.txt", "a")
            output.write(sentiment_value)
            testList += [sentiment_value]
            # if len(testList) > 120:
            #     testList = testList[-100:]
            #     print(len(testList))

            output.write('\n')
            output.close()

        return True

    def on_error(self, status):
        logTwitterError(status)
        print(status)

def runStream():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["S&P 500", "S&P", "Dow", "Dow Jones", "DJI", "Standard And Poors", "NASDAQ", "FANG",
                                "QQQ", "Stock"], is_async=True)

# Economy, markets, SPY
# TODO: Make sure tweet is in english
# Bad words: Down, lower,
# Good words: Up, higher


