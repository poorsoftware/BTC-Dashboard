#!/usr/bin/env python3
from tkinter import *
import pigpio
import requests
import sys
import datetime
from urllib.request import urlopen
from json import loads

gpio = pigpio.pi()

class BTCTicker:
	def __init__(self, master):
		self.master = master
		self.close_button = Button(text="C", command=self.close)
		self.close_button.grid(row=0, column=0)
		self.label = Label(master, text="BTC Dashboard",anchor=W, justify=LEFT, font=('Helvetica',32, 'bold'), fg = 'blue')
		self.label.grid(row=0, column=1, columnspan=1)

	def labels():
		hwg()
		title = "Market Data"
		down_label = Label(text=(title),anchor=NW, width = 21, justify=LEFT,font=('Helvetica', 24, 'bold'))
		down_label.grid(row=2, column=1, sticky=W)

		currency = "{:,.2f}".format(pricebtc)
		text1 = "BTC Price: $" + str(currency)
		currency = "{:,.2%}".format(pricebtc24hrchange)
		text2 = "24hr change: " + str(currency)
		currency = "{:,.0f}".format(satsusd)
		text3 = "Sats per $: " + str(currency)
		currency = "{:,.0f}".format(marketcapbtc)
		text4 = "Marketcap: $" + str(currency)
		down_label = Label(text=(text1 + '\n' + text2 + '\n' + text3 + '\n'  + text4 + '\n'),anchor=NW, justify=LEFT,font=('Helvetica',20))
		down_label.grid(row=3, column=1, sticky=W)

		title = "Blockchain Data"
		down_label = Label(text=(title),anchor=NW, width = 21, justify=LEFT,font=('Helvetica', 24, 'bold'))
		down_label.grid(row=4, column=1, sticky=W)

		currency = "{:,.0f}".format(hashrate24hr)
		text5 = "Hashrate 24hr: " + str(currency) + " EH/s"
		currency = "{:,.02%}".format(next_difficulty_estimate)
		text5a = "Next difficulty: " + str(currency)
		date_time_obj = datetime.datetime.strptime(next_retarget_time_estimate, '%Y-%m-%d %H:%M:%S')
		text5b = "Next adjustment: " + str(date_time_obj.date()) #.strftime("%Y-%m-%d %H:%M")
		currency = "{:,.0f}".format(mempool)
		text6 = "Mempool: " + str(currency) + " transactions"
		currency = "{:,.0f}".format(blocks)
		text7 = "Last block: " + str(currency)
		currency = "${:,.2f}".format(average_transaction_fee_usd_24h)
		text8 = "Average Fee: " + str(currency)
		currency = "{:,.0f}".format(suggested_transaction_fee)
		text8a = "Suggested Fee: " + str(currency) + " sat/vB"
		down_label = Label(text=(text5 + '\n' + text5a + '\n' + text5b + '\n' + text6 + '\n' + text7 + '\n' + text8 + '\n' + text8a + '\n'),anchor=NW, justify=LEFT,font=('Helvetica',20))
		down_label.grid(row=5, column=1, sticky=W)

		title = "Fear Index"
		down_label = Label(text=(title),anchor=NW, width = 21, justify=LEFT,font=('Helvetica', 24, 'bold'))
		down_label.grid(row=6, column=1, sticky=W)

		text10 = "Fear & Greed Index: " + str(fearindex)
		text11 = "Fear Value: " + str(fearindexvalue)
		down_label = Label(text=(text10 + '\n' + text11 + '\n'),anchor=NW, justify=LEFT,font=('Helvetica',20))
		down_label.grid(row=7, column=1, sticky=W)
		
		now = datetime.datetime.now()
		text99 = "Current time: " + str(now)
		down_label = Label(text=(text99),anchor=NW, justify=LEFT,font=('Helvetica',12))
		down_label.grid(row=9, column=1, sticky=W)        

#		text1 = "str(btcmaxtime) #.strftime("%Y-%m-%d %H:%M")
#		text2 =  "Portfolio____: " + u'\u20bf' + str(btcprint)
		
# This is where you set the update time. 1000 - 1 sec	
		down_label.after(180000,BTCTicker.labels)

	def close(self):
		root.destroy()

def bright():  # not yet activated
# settings for bright screen. 255 = max	
	gpio.set_PWM_dutycycle(19, 255)

def dark():
# brightness setting. 30 is dimmed display.
	gpio.set_PWM_dutycycle(19, 30)

def hwg():
	global commits
	global fearindex
	global fearindexvalue
	global satsusd
	global hashrate24hr
	global mempool
	global pricebtc
	global pricebtc24hrchange
	global marketcapbtc
	global suggested_transaction_fee
	global average_transaction_fee_usd_24h
	global next_difficulty_estimate
	global next_retarget_time_estimate
	global blocks

	try:
#	get the fearindex
		fearindex = str(loads(urlopen('https://api.alternative.me/fng/').read())['data'][0]['value_classification'])
		fearindexvalue = str(loads(urlopen('https://api.alternative.me/fng/').read())['data'][0]['value'])
	except:
		print("Error reading Fearindex")
	try:

#	get blockchain data https://blockchair.com/api/docs#link_M03
        blockchair_api_request = urlopen('https://api.blockchair.com/bitcoin/stats').read()
		pricebtc = float(loads(blockchair_api_request)['data']['market_price_usd'])
		pricebtc24hrchange = float(loads(blockchair_api_request)['data']['market_price_usd_change_24h_percentage'])
		marketcapbtc = float(loads(blockchair_api_request)['data']['market_cap_usd'])
		suggested_transaction_fee = float(loads(blockchair_api_request)['data']['suggested_transaction_fee_per_byte_sat'])
		average_transaction_fee_usd_24h = float(loads(blockchair_api_request)['data']['average_transaction_fee_usd_24h'])
		hashrate24hr = float(loads(blockchair_api_request)['data']['hashrate_24h'])
		mempool = float(loads(blockchair_api_request)['data']['mempool_transactions'])
		blocks = float(loads(blockchair_api_request)['data']['blocks'])
		next_retarget_time_estimate = str(loads(blockchair_api_request)['data']['next_retarget_time_estimate'])
		next_difficulty_estimate = float(loads(blockchair_api_request)['data']['next_difficulty_estimate'])
		difficulty = float(loads(blockchair_api_request)['data']['difficulty'])
		
		pricebtc24hrchange = pricebtc24hrchange / 100
		hashrate24hr = hashrate24hr / 1000000000000000000  # in EH/s
		satsusd = 1 / pricebtc * 100000000
		next_difficulty_estimate = 1 - difficulty / next_difficulty_estimate
		print(pricebtc)

	except:
		print("Error reading Blockchair")
	
#	try: 
#	get GitHub data
#		commits = str(loads(urlopen('https://api.coincodecap.com/v1/details_v1/BTC').read())['data']['total_commits'])
#	except:
#		print("Error reading CoinCodeCap")


root = Tk()
root.configure(cursor='none')
root.attributes('-fullscreen', True)
my_gui = BTCTicker(root)
BTCTicker.labels()
root.mainloop()
#time.sleep(3)
