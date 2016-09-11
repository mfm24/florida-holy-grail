import tweepy
import json
from fhg_tweeter import get_best_headlines


url = ('http://www.baynews9.com/content'
            '/news/baynews9/feeds/rss.html/strange.html')

headlines = get_best_headlines(url)
if headlines:
    print(headlines)
secrets = json.load(open('twitter_keys.json'))
auth = tweepy.OAuthHandler(secrets['API Key'], secrets['API Secret'])
auth.secure = True
auth.set_access_token(secrets['Access Token'], secrets['Access Token Secret'])
api = tweepy.API(auth)

#api.update_status(new_update)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)
