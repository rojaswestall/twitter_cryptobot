# authors: mpeter66 and rojaswestall

import tweepy
from datetime import datetime
from json import loads
from requests import get
from mgconfig import *
from threading import Thread
from time import sleep



# Authenticating with Tweepy
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


#### NEED TO FIND A BETTER WAY OF MAKING THE COIN LIST
# The URLS are links to json objects to the price of a currency in terms of a specified currency
# The json objects will have the price in USD because syms=USD
# Add the cryptocurrencies you want to track here
btc = ('BTC', 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD') # Bitcoin
eth = ('ETH', 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD') # Ethereum
ltc = ('LTC', 'https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD') # Litecoin
xrp = ('XRP', 'https://min-api.cryptocompare.com/data/price?fsym=XRP&tsyms=USD') # Ripple
sc  = ('SC', 'https://min-api.cryptocompare.com/data/price?fsym=SC&tsyms=USD')   # SiaCoin
coin_list = [btc, eth];


# Returns the price for any coin given as an arugment.
# Returns in this format: {'USD': 2764} (dictionary)
def coin_price(coin): 
	price = loads(get(coin[1]).text) 
	return price


# Simple %Change calculator
def percent_change(original, new):
	percentchange = (abs(original - new) / original) * 100
	return percentchange


# A function that monitors the price fluctuation of a coin and tweets if there is a certain 
# percent change. 
def percent_monitor(coin):
	old_price = coin_price(coin)['USD']
	new_price = old_price
	# Check if price change is greater than 5%. 
	# If it's not, wait a minute, update the new prices, and try again
	while percentchange(old_price, new_price) < 5:
		sleep(60)
		new_price = coin_price(coin)['USD']
	# If it's greater tweet the change, whether it increased or decreased, and the period of time it took


	# Want to reset the old price every day 12 hours regardless of whether or not it has shifted by 5%
	# Tweet if it has dropped by 5% or increased by 5%

	### Need to write something that checks every minute or 
	### two and then tweets if the change is large enough


# Tweets the price of all desired coins at that time
def first_tweet(coin_list):
	rightnow = datetime.now().strftime("%b. %d %Y %I:%M%p")
	message = 'Crypto prices right now (' + rightnow + '):\n'
	for coin in coin_list:
		price = str(coin_price(coin)['USD'])
		message = message + '\n' + coin[0] + ': ' + price
	print(message)
	#api.update_status(message)
	# coin[0] will print out the cyrptocurrency code for that coin: 'BTC'
	# price['BTC'] will give the dictionary price value for BTC if price = get_price(btc)


# The function that will start the monitoring of all specified coins
def monitor_coins(coin_list):
	first_tweet(coin_list)
	# Start monitoring each coin
	for coin in coin_list:
		thread = Thread(target = percent_monitor(coin))
		thread.start()

first_tweet(coin_list)

