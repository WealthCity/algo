#!/usr/bin/python
# -*- coding: utf-8 -*-

# forecast.py

from __future__ import print_function
import datetime
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.lda import LDA
from sklearn.metrics import confusion_matrix
from sklearn.qda import QDA
from sklearn.svm import LinearSVC, SVC


def create_lagged_series(data_frame,column,volume = 'volume',lags=5):
	"""
	This creates a pandas DataFrame that stores the 
	percentage returns of the adjusted closing value of 
	a stock obtained from Yahoo Finance, along with a 
	number of lagged returns from the prior trading days 
	(lags defaults to 5 days). Trading volume, as well as 
	the Direction from the previous day, are also included.
	"""

	# Obtain stock information from Yahoo Finance
    

	# Create the new lagged DataFrame
	tslag = pd.DataFrame(index = data_frame.index)
	tslag["Today"] = data_frame[column].astype('float')
	tslag["Volume"] = data_frame[volume]
	print(tslag.head())
	# Create the shifted lag series of prior trading period close values
	for i in range(0, lags):
		tslag["Lag_{}".format(str(i+1))] = tslag["Today"].shift(i+1)

	# Create the returns DataFrame
	tsret = pd.DataFrame(index=tslag.index)
	tsret["Volume"] = tslag['Volume']
	tsret["Today"] = tslag["Today"].pct_change()

	# If any of the values of percentage returns equal zero, set them to
	# a small number (stops issues with QDA model in scikit-learn)
	#for i,x in enumerate(tsret["Today"]):
	#    if (abs(x) < 0.0001):
	#        tsret["Today"][i] = 0.0001
	tsret[abs(tsret['Today'])<0.0001]=0.0001
	
	# Create the lagged percentage returns columns
	for i in range(0, lags):
		tsret["Lag_{}%".format(str(i+1))] = tslag["Lag_{}".format(str(i+1))].pct_change()
	#Create the "Direction" column (+1 or -1) indicating an up/down day
	tsret["Direction"] = np.sign(tsret["Today"])
	
	#tsret = tsret[tsret.index >= start_date]

	return tsret


def forecast(data_frame,variables,target,training_data=0.7, test_data=0.3):

	# Use the prior two days of returns as predictor 
	# values, with direction as the response
	X = data_frame[variables]
	y = data_frame[target]

	# The test data is split into two parts: Before and after 1st Jan 2005.
	print(len(data_frame.index))
	number_of_records= len(data_frame.index)
	start_index = round(number_of_records*(1-test_data))
	start_test =  data_frame.index[start_index]
	print(start_test)

	# Create training and test sets
	X_train = np.nan_to_num(X[X.index < start_test].values)
		
	#print(X_train.head())
	X_test = np.nan_to_num(X[X.index >= start_test].values)

	y_train = np.nan_to_num(y[y.index < start_test].values)
	
	y_test = np.nan_to_num(y[y.index >= start_test].values)
   
	# Create the (parametrised) models
	print("Hit Rates/Confusion Matrices:\n")
	models = [("Logistic Regression", LogisticRegression()), 
		("Linear Discrimenent", LDA()),
		("QDA", QDA()),
		("LSVC", LinearSVC()),
		("RSVM", SVC(
			C=1000000.0, cache_size=200, class_weight=None,
			coef0=0.0, degree=3, gamma=0.0001, kernel='rbf',
			max_iter=-1, probability=False, random_state=None,
			shrinking=True, tol=0.001, verbose=False)),
		("RF", RandomForestClassifier(
			n_estimators=1000, criterion='gini', 
			max_depth=None, min_samples_split=2, 
			min_samples_leaf=1, max_features='auto', 
			bootstrap=True, oob_score=False, n_jobs=1, 
			random_state=None, verbose=0)
		)]

	# Iterate through the models
	for m in models:
	# Train each of the models on the training set
		try:
			m[1].fit(X_train, y_train)

			# Make an array of predictions on the test set
			pred = m[1].predict(X_test)
			
			#
			print(pred)
			# Output the hit-rate and the confusion matrix for each model
			print("{}:\n%{}".format(m[0], m[1].score(X_test, y_test)))
			
			print("{}\n".format( confusion_matrix(pred, y_test)))
		except:
			pass
