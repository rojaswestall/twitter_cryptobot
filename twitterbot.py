# authors: mpeter66 and rojaswestall

import tweepy
from mgconfig import *

# Authenticating with Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


