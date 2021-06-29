import keys
import tweepy
import sys
import preprocessor as p
from textblob import TextBlob

class SentimentListener(tweepy.StreamListener):
    
    def __init__(self, api, sentiment_dict, topic, limit=10):
        self.sentiment_dict = sentiment_dict
        self.topic = topic
        self.TWEET_LIMIT = limit
        self.tweet_count = 0
        super().__init__(api)

    def on_status(self, status):
        """receives tweets as stream so we need to handle them
            in a try/except block  """

        try:
            #if the tweet is bigger than 280 characters long
            tweet_text = status.extended_tweet.full_text
        except:
            #if the tweet is less than 280 characters long
            tweet_text = status.text

        if tweet_text.startswith("RT"):
            #ignore retweets
            return

        p.set_options(p.OPT.URL, p.OPT.RESERVED)

        tweet_text = p.clean(tweet_text) #no urls/reserved words in the tweet

        #don't print the tweet if the topic is not there
        if self.topic not in tweet_text.lower():
            return

        #sentiment analyis part:
        blob = TextBlob(tweet_text)

        sentiment = ' '
        if blob.sentiment.polarity < -0.1:
            sentiment = ' - '
            self.sentiment_dict['negative'] += 1
        elif -0.1 < blob.sentiment.polarity < 0.1:
            sentiment = ' '
            self.sentiment_dict['neutral'] += 1
        elif blob.sentiment.polarity > 0.1:
            sentiment = ' + '
            self.sentiment_dict['positive'] += 1

        #display the tweet:
        print(f"{sentiment} name: {status.user.screen_name}\n tweet: {tweet_text}\n")

        self.tweet_count += 1

        #if the tweet limit is reached then return False and end the stream
        return self.tweet_count != self.TWEET_LIMIT

def main():
    #configure the OAuth handler:
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_key_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    sentiment_dict= {'negative': 0, 'neutral': 0, 'positive': 0}




    #the name of topic we're looking for 
    search_term = sys.argv[1]

    #limit of the tweets:
    limit = int(sys.argv[2])

    streamListener = SentimentListener(api, sentiment_dict, topic=search_term, limit=limit)
    #instanciate a stream listener

    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    
    #filter the english tweets that contain the search_term
    stream.filter(track=[search_term], languages=['en'], is_async=False)
    
    print(f' Tweet for {search_term}')
    print(f"positive: {sentiment_dict['positive']}")
    print(f"negative: {sentiment_dict['negative']}")
    print(f"neutral: {sentiment_dict['neutral']}")

if __name__ == "__main__":
    main()
