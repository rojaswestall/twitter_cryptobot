# author: Gabe Rojas-Westall (github: rojaswestall)

import tweepy
from datetime import datetime
from json import loads
from requests import get
from mgconfig import *
from threading import Thread
from time import sleep
from message_format import TimeMessage, IncOrDec
from multiprocessing import Pool


# Authenticating with Tweepy
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# The URL is a link to the json object of the price of a currency in terms of another specified currency
# Here, the json objects will have the price in USD because syms=USD
# Add the coin code in all CAPS to coins for the coins you want to be monitored
coins = ['BTC', 'ETH', 'LTC', 'XRP', 'SC']
coin_list = []

for code in coins:
	coin = (code, 'https://min-api.cryptocompare.com/data/price?fsym=' + code + '&tsyms=USD')
	coin_list.append(coin)

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
	print('Monitor started for ' + coin[0] + '!')
	ogtime = datetime.now()
	old_price = coin_price(coin)['USD']
	new_price = old_price
	# Check if price change is greater than the specified %. 
	# If it's not, wait a minute, update the new prices, and try again
	while percent_change(old_price, new_price) < 3:
		sleep(60)
		new_price = coin_price(coin)['USD']
	# If it's greater, tweet the change, whether it increased or decreased, and the period of time it took
	recordtime = datetime.now()
	timedif = recordtime - ogtime
	hours = int(timedif.seconds / 3600) # The number of hours (-minutes) it took to change 5%
	minutes = int((timedif.seconds - (hours * 3600)) / 60) # The number of minutes (-hours) it took to change 5%

	# Making the tweet look pretty :)
	change = IncOrDec(new_price, old_price)
	hours, minutes, hourmsg, minutemsg = TimeMessage(hours, minutes)
	
	message = '{} {} {:04.2f}{} in the past {}{}{}{}!\n\nThe new price is ${}'.format(coin[0], change, percent_change(old_price, new_price), '%', str(hours), hourmsg, str(minutes), minutemsg, str(new_price))
	api.update_status(message)
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
	# price['USD'] will give the dictionary price value for BTC if price = coin_price(btc)


# The function that will start the monitoring of all specified coins
def monitor_coins(coin_list):
	first_tweet(coin_list)
	# Start monitoring each coin
	for coin in coin_list:
		thread = Thread(target = change_monitor, args = (coin,))
		thread.start()

monitor_coins(coin_list)


