# The formatting for the messages

# This will correct the grammar for the amount of time it's taken for a change to occur
def TimeMessage(hours, minutes):
	if hours > 1 and minutes == 0:
		hourmsg = ' hours'
		minutemsg = ''
		minutes = ''
	elif hours > 1 and minutes == 1:
		hourmsg = ' hours and '
		minutemsg = ' minute'
	elif hours > 1 and minutes > 1:
		hourmsg = ' hours and '
		minutemsg = ' minutes'
	elif hours == 1 and minutes == 0:
		hourmsg = ' hour'
		minutemsg = ''
		minutes = ''
	elif hours == 1 and minutes == 1:
		hourmsg = ' hour and '
		minutemsg = ' minute'
	elif hours == 1 and minutes > 1:
		hourmsg = ' hour and '
		minutemsg = ' minutes'
	elif hours == 0 and minutes == 1:
		hours = ''
		hourmsg = ''
		minutemsg = ' minute'
	else: #hours == 0 and minutes > 1
		hours = ''
		hourmsg = ''
		minutemsg = ' minutes'
	return hours, minutes, hourmsg, minutemsg

def IncOrDec(new_price, old_price):
	if new_price > old_price:
		change = 'has increased by'
	else:
		change = 'has decreased by'
	return change