import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import requests
import json
t = time.time()
def plot_chart_dynamic(symbol):
	t = time.time()
	plt.style.use('dark_background')
	url_l = 'https://api.iextrading.com/1.0/stock/'
	url = url_l+ symbol + '/chart/dynamic'
	r = requests.get(url)
	r = r.json()
	
	df = pd.DataFrame(r['data'])
	df.set_index('minute', inplace = True)
	df.index = pd.to_datetime(df.index, errors = 'ignore', format = '%H:%M') #format = '%Y-%m-%d')
	df['open'].plot(grid = True)
	plt.ylabel('Price/USD')
	xlabell = 'Last Refreshed: ' + str(datetime.datetime.now())
	plt.xlabel(xlabell)
	plt.title('Price (Dynamic)    Company Symbol: '+symbol.upper())
	plt.savefig('display.png')
	t1 = time.time()
	print(t1-t)


plot_chart_dynamic('amzn')