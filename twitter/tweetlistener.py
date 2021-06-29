"""tweepy StreamListener subclass that processes tweets as they arrive"""
import tweepy
from textblob import TextBlob

class TweetListener(tweepy.StreamListener):
    def __init__(self, api, limit=10):
        self.tweet_count = 0
        self.TWEET_LIMIT = 10
        super().__init__(api)

    def on_connect(self):
        print("Connection successful")

    def on_status(self, status):
        try:
            tweet_text = status.extended_tweet.full_text
        except:
            tweet_text = status.text

        print(f'Screen Name: {status.user.screen_name}:')
        print(f'    Language: {status.lang}')
        print(f'      Status: {tweet_text}')

        if status.lang != 'en':
            print(f"translated tweet: {TextBlob(tweet_text).translate()}")

        print()
        self.tweet_count += 1

        #returns false if they are equal which is used to end the stream
        return self.tweet_count != self.TWEET_LIMIT

