#!/usr/bin/python # -*- coding: utf-8 -*
# sharpe.py
from __future__ import print_function
import datetime 
import numpy as np 
import pandas as pd 


def annualised_sharpe(data_frame, column, N=252): 
	""" Calculate the annualised Sharpe ratio of a returns stream based on a number of trading periods, 
	N. N defaults to 252, which then assumes a stream of daily returns.
	The function assumes that the returns are the excess of those compared to a benchmark. """ 
	returns = data_frame[column].astype('float').pct_change()
	return (np.sqrt(N) * returns.mean() / returns.std()) 

def equity_sharpe(data_frame,column,risk_free=0.05,periods=252): 
	""" Calculates the annualised Sharpe ratio based on the daily returns of an equity"""
	#start = datetime.datetime(2000,1,1) 
	#end = datetime.datetime(2013,1,1)
	# Obtain the equities daily historic data for the desired time period # and add to a pandas DataFrame
	# pdf = web.DataReader(ticker, ’google’, start, end)
	# Use the percentage change method to easily calculate daily returns 
	
	data_frame['daily_ret'] = data_frame[column].astype('float').pct_change()
	# Assume an average annual risk-free rate over the period of 5% 
	data_frame['excess_daily_ret'] = data_frame['daily_ret'] - risk_free/periods
	# Return the annualised Sharpe ratio based on the excess daily returns 
	print('Inside data frame')
	return (annualised_sharpe(data_frame,'excess_daily_ret')) 


def market_neutral_sharpe(data_frame_1,column_1,data_frame_2,column_2): 
	""" Calculates the annualised Sharpe ratio of a market neutral long/short 
	strategy inolving the long of ’ticker’ with a corresponding short of the ’benchmark’. """ 
	# Calculate the percentage returns on each of the time series 
	data_frame = pd.DataFrame(index=data_frame_1.index)
	data_frame['daily_return'] = data_frame_1[column_1].astype('float').pct_change() 
	data_frame['benchmark'] = data_frame_2[column_2].astype('float').pct_change()
		
	# Create a new DataFrame to store the strategy information 
	# The net returns are (long - short)/2, since there is twice # the trading capital for this strategy 
	
	data_frame['net_ret'] = ((data_frame['daily_return'] - data_frame['benchmark'])/2.0)
	print(str(data_frame))
	print(data_frame.tail())
	# Return the annualised Sharpe ratio for this strategy 
	return (annualised_sharpe(data_frame.iloc[2:],'net_ret'))


