import statsmodels.tsa.stattools as ts
from numpy import log,sqrt,subtract,std,polyfit
import pandas as pd
import sys

class Test_Stationarity:
	"""Test all series in dic for stationarity"""
    
	def __init__(self,data_frame,column):
		self.data_frame = data_frame
		self.colum = column
		self.series = data_frame[column].astype('float')
		print(type(self.series))
		#pd.to_numeric(self.series,errors='ignore')
	
			
		self.dickey_fuller_p_value = None
		self.dickey_fuller_test_stat = None
		self.dickey_fuller_result = None
			
		self.hurst_exponent = None
		self.hurst_exponent_result = None

	  
	def dickey_fuller_test(self):
		#self.dickey_fuller_result = False
		try:
			df_results = ts.adfuller(self.series)
			print (df_results)
			self.dickey_fuller_result = True
		except:
			print('Error with Dickey Fuller Test: '.format(sys.exc_info()[0]))
			self.dickey_fuller_result = None

		if self.dickey_fuller_result == True:
			self.dickey_fuller_test_stat = df_results[0]
			self.dickey_fuller_p_value = df_results[1]
			print("Augmented Dickey Fuller Test \n Test Statistic: {} \n P-value: {}".format(self.dickey_fuller_test_stat,self.dickey_fuller_p_value))
			
		if df_results[1]>0.05:
			self.dickey_fuller_result = 'Non-stationary'
			print(self.dickey_fuller_result)
			
		
		else:
			self.dickey_fuller_result = 'Stationary'
			print(self.dickey_fuller_result)
		
		# hurst exponent
	def test_hurst_exponent(self):
		"""Returns the Hurst Exponent of the time series vector ts"""
		try:
			# Create the range of lag values
			lags = range(2, 100)
			ts=log(self.series)
			
			# Calculate the array of the variances of the lagged differences
			tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
			
			# Use a linear fit to estimate the Hurst Exponent
			poly = polyfit(log(lags), log(tau), 1)
			
			# Return the Hurst exponent from the polyfit output
			self.hurst_exponent = poly[0]*2.0
			
			self.hurst_exponent_result = True
			print('Hurst Exponent : {} '.format(self.hurst_exponent))
		except:
			print('Hurst exponent cannot be calculated')
			self.hurst_exponent = None
