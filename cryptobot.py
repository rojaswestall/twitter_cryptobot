# authors: mpeter66 and rojaswestall

import tweepy
from json import loads
from requests import get
from mgconfig import *


# Authenticating with Tweepy
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# The URLS are links to json objects to the price of a currency in terms of a specified currency
# The json objects will have the price in USD because syms=USD
# Add the cryptocurrencies you want to track here
btc = ('BTC', 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD') # Bitcoin
eth = ('ETH', 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD') # Ethereum
ltc = ('LTC', 'https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD') # Litecoin
xrp = ('XRP', 'https://min-api.cryptocompare.com/data/price?fsym=XRP&tsyms=USD') # Ripple
sc  = ('SC', 'https://min-api.cryptocompare.com/data/price?fsym=SC&tsyms=USD')   # SiaCoin

# Returns the price for any coin given as an arugment.
# Returns in this format: {'USD': 2764} (json object)
def coin_price(coin): 
	price = loads(get(coin[1]).text) 
	return price

def percent_monitor(coin):
	coin_price(coin)
	
btcprice = coin_price(btc);
print(btcprice)
