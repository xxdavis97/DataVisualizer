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

class dogListener(StreamListener):
    def on_data(self, data):
        global testList
        all_data = json.loads(data)
        tweet = all_data["text"]
        try:
            sentiment_value, confidence =s.sentiment(tweet)
            if confidence * 100 >= 80:
                output = open("dog-out.txt", "a")
                output.write(sentiment_value)
                output.write('\n')
                output.close()
        except Exception as e:
            logError(e, "DogListener")

        return True

    def on_error(self, status):
        logTwitterError(status)
        print(status)

class catListener(StreamListener):
    def on_data(self, data):
        global testList
        all_data = json.loads(data)
        tweet = all_data["text"]
        try:
            sentiment_value, confidence = s.sentiment(tweet)
            if confidence * 100 >= 80:
                output = open("cat-out.txt", "a")
                output.write(sentiment_value)
                output.write('\n')
                output.close()
        except Exception as e:
            logError(e, "CatListener")

        return True

    def on_error(self, status):
        logTwitterError(status)
        print(status)

def runDogStream():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitterStream = Stream(auth, dogListener())
    twitterStream.filter(track=["Dog", "Puppy"], is_async=True)

def runCatStream():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitterStream = Stream(auth, catListener())
    twitterStream.filter(track=["Cat", "Kitten"], is_async=True)


# Economy, markets, SPY
# TODO: Make sure tweet is in english
# Bad words: Down, lower,
# Good words: Up, higher


