import datetime
import pandas as pd
from ... import securities_master as sm


now = datetime.datetime.now()
exchange = [{
		'abbrev':'asx',
		'name':'Australian Stock Exchange',
		'city':'Sydney',
		'country':'Australia',
		'currency':'AUD',
		'timezone_offset':0
		}]
data_vendor = [{}]



def open_ASX_listing_from_csv(path):
	"""Function to open ASX listing csv and save to data frame """
	asx_listing = pd.read_csv(path)
	print(asx_listing.head())
	print(asx_listing.tail())
	return (asx_listing)


def insert_exchange_data(exchanges):
	"""Function to insert exchange information into securities master database"""
	for exchange in exchanges:
		Exchange.create(abbrev=exchange['abrev'],
				name =exchange['name'],
				city =exchange['city'],
				country=exchange['country'],
				currency=exchange['currency'],
				timezone_offset=exchange['timezone_offset'],
				created_date = now,
				last_updated_date=now)
	
	pass

def insert_data_vendor():
	"""Function to insert data vendor  information into securities master data base"""
	pass

def insert_ASX_listing_into_securities_master(data_frame,now):
	"""Function to take data frame and save it to securities master database"""
	
	# first time - save all data
	
	# second time -if ntegrity error, only save update
	print(now)
	pass


if __name__=='__main__':
	asx_listing=open_ASX_listing_from_csv('ASXListedCompanies.csv')
	insert_ASX_listing_into_securities_master(asx_listing)
