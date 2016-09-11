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

headlines = get_best_headlines(url)
for headline in headlines:
    if len(headline) < 140:
        print(headline)
        api.update_status(headline)
        break
