import tweepy
import json

secrets = json.load(open('twitter_keys.json'))
auth = tweepy.OAuthHandler(secrets['API Key'], secrets['API Secret'])
auth.secure = True
auth.set_access_token(secrets['Access Token'], secrets['Access Token Secret'])
api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
