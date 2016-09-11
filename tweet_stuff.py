import tweepy
import json
from fhg_tweeter import get_best_headlines


url = ('http://www.baynews9.com/content'
            '/news/baynews9/feeds/rss.html/strange.html')

secrets = json.load(open('twitter_keys.json'))
auth = tweepy.OAuthHandler(secrets['API Key'], secrets['API Secret'])
auth.secure = True
auth.set_access_token(secrets['Access Token'], secrets['Access Token Secret'])
api = tweepy.API(auth)

headlines = get_best_headlines(url, True)
if headlines:
    #print(headlines[0])
    api.update_status(headlines[0])

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)
