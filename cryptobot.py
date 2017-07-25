# author: rojaswestall

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


# The URL is a link to the json object of the price of a currency in terms of another specified currency
# Here, the json objects will have the price in USD because syms=USD
#btc = ('BTC', 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD') # Bitcoin
# Add the coin code in all CAPS to coins for the coins you want to be monitored
coins = ['BTC', 'ETH', 'LTC', 'XRP', 'SC']
coin_list = [];

for code in coins:
	coin = (code, 'https://min-api.cryptocompare.com/data/price?fsym=' + code + '&tsyms=USD')
	coin_list = coin_list.append(coin)

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
def change_monitor(coin):
	ogtime = datetime.now()
	old_price = coin_price(coin)['USD']
	new_price = old_price
	# Check if price change is greater than 1%. 
	# If it's not, wait a minute, update the new prices, and try again
	while percent_change(old_price, new_price) < 1:
		sleep(60)
		new_price = coin_price(coin)['USD']
		#### Want to reset the old price every 12 hours regardless of whether or not it has shifted by 5%
		#### because 5% differences after 12 hours aren't as significant
		####timedif = ogtime - datetime.now()
		####if timedif.seconds > 43200: # 43200sec = 12 hours
		####	ogtime = datetime.now()
	# If it's greater, tweet the change, whether it increased or decreased, and the period of time it took
	timedif = ogtime - datetime.now()
	hours = int(timedif.seconds / 3600) # The number of hours (-minutes) it took to change 5%
	minutes = int((timedif.seconds - (hours * 3600)) / 60) # The number of minutes (-hours) it took to change 5%

	if new_price > old_price:
		message = 'has increased by 1%'
	else:
		message = 'has decreased by 1%'

	api.update_status(coin[0] + message + ' in the past ' + str(hours) + ' hours and ' + str(minutes) + ' minutes!\n\nThe new price is $' + str(new_price))
	print('Price change tweeted for ' + coin[0])
	change_monitor(coin)

	# BUT HOW TO MAKE THE TIMES AND PRICE COMPARISON CONTINUOUSLY CHANGING???


# Tweets the price of all desired coins at that time
def first_tweet(coin_list):
	rightnow = datetime.now().strftime("%b. %d, %Y %I:%M%p")
	message = 'Crypto prices right now (' + rightnow + '):\n'
	for coin in coin_list:
		price = str(coin_price(coin)['USD'])
		message = message + '\n' + coin[0] + ': $' + price
	api.update_status(message)
	# coin[0] will print out the cyrptocurrency code for that coin: 'BTC'
	# price['BTC'] will give the dictionary price value for BTC if price = get_price(btc)


# The function that will start the monitoring of all specified coins
def monitor_coins(coin_list):
	first_tweet(coin_list)
	# Start monitoring each coin
	for coin in coin_list:
		thread = Thread(target = change_monitor(coin))
		thread.start()

monitor_coins(coin_list)


