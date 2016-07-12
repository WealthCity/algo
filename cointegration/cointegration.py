import datetime 
import numpy as np 
import matplotlib
matplotlib.rcParams['backend'] = "Qt5Agg"
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates 
import matplotlib
import pandas as pd  
import pprint 
import statsmodels.tsa.stattools as ts
from pandas.stats.api import ols
import pylab
from time_series_analysis.test_stationarity import Test_Stationarity

def plot_price_series(df1, ts1, df2,ts2): 
	months = mdates.MonthLocator() # every month 
	fig, ax = plt.subplots()
	ax.plot(df1.index, df1[ts1], label=ts1)
	ax.plot(df1.index, df2[ts2], label=ts2) 
	ax.xaxis.set_major_locator(months) 
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) 
	#ax.set_xlim(datetime.datetime(2012, 1, 1), datetime.datetime(2013, 1, 1)) 
	ax.grid(True) 
	fig.autofmt_xdate()
	plt.xlabel('Month/Year') 
	plt.ylabel('Price ($)') 
	plt.title('{} and {} Daily Prices'.format(ts1,ts2)) 
	plt.legend() 
	plt.show() 
	

def plot_scatter_series(df1, ts1, df2,ts2):
	plt.xlabel('{} Price ($)'.format(ts1)) 
	plt.ylabel('{} Price ($)'.format(ts2)) 
	plt.title('{} and {} Price Scatterplot'.format(ts1, ts2)) 
	plt.scatter(df1[ts1], df2[ts2]) 
	plt.show()

def plot_residuals(df):
	months = mdates.MonthLocator() # every month 
	fig, ax = plt.subplots() 
	ax.plot(df.index, df["res"], label="Residuals") 
	ax.xaxis.set_major_locator(months) 
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) 
	#ax.set_xlim(datetime.datetime(2012, 1, 1), datetime.datetime(2013, 1, 1)) 
	ax.grid(True) 
	fig.autofmt_xdate()
	plt.xlabel('Month/Year') 
	plt.ylabel('Price ($)') 
	plt.title('Residual Plot') 
	plt.legend()
	plt.plot(df["res"]) 
	plt.show()

def cointegrate(ticker1,df1,ts1,ticker2,df2,ts2):
	
	df = pd.DataFrame(index=df1.index) 
	column1 = '{}_{}'.format(ticker1,ts1)
	column2 = '{}_{}'.format(ticker2,ts2)
	
	df[column1] = df1[ts1].astype('float') 
	df[column2] = df2[ts2].astype('float')
	
	# Plot the two time series 
	#plot_price_series(df1, ts1, df2,ts2)

	# Display a scatter plot of the two time series 
	#plot_scatter_series(df1, ts1, df2,ts2)
	# Calculate optimal hedge ratio "beta" 
	res = ols(y=df[column2], x=df[column1]) 
	print(res)
	#print(res.params)
	#res = res.fit()
	#print(res.summary())
	beta_hr = res.beta.x
	print(res.beta.intercept)
	# Calculate the residuals of the linear combination 
	#df = pd.DataFrame(index = df1.index)
	df['model']= res.beta.intercept+beta_hr*df[column1]
	df["res"] = df[column2] - df['model']

	# Plot the residuals 
	plot_residuals(df)
	
	# Calculate and output the CADF test on the residuals 
	test = Test_Stationarity(df,'res')
	test.dickey_fuller_test()
	test.test_hurst_exponent()
	
