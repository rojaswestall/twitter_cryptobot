# authors: mpeter66 and rojaswestall

import tweepy
from json import loads
from requests import get
from mgconfig import *


# Authenticating with Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

# The URLS are links to json objects to the price of a currency in terms of a specified currency
# The json objects will have the price in USD and EUR because syms=USD,EUR
btc = ('BTC', 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR') # Bitcoin
eth = ('ETH', 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR') # Ethereum
ltc = ('LTC', 'https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,EUR') # Litecoin
xrp = ('XRP', 'https://min-api.cryptocompare.com/data/price?fsym=XRP&tsyms=USD,EUR') # Ripple
sc  = ('SC', 'https://min-api.cryptocompare.com/data/price?fsym=SC&tsyms=USD,EUR')   # SiaCoin



