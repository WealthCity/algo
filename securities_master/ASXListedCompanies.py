import datetime
import pandas as pd
from securities_master import Exchange,Data_Vendor,Symbol,Daily_Price
 

now = datetime.datetime.now()
exchange = [{
		'abbrev':'asx',
		'name':'Australian Stock Exchange',
		'city':'Sydney',
		'country':'Australia',
		'currency':'AUD',
		'timezone_offset':0
		}]
data_vendor = [{'name':'quandl',
		'website_url':'https://www.quandl.com/data/XASX?keyword=australian',
		'support_email':''
		}]



def open_ASX_listing_from_csv(path):
	"""Function to open ASX listing csv and save to data frame """
	asx_listing = pd.read_csv(path)
	print(asx_listing.head())
	print(asx_listing.tail())
	return (asx_listing)


def insert_exchange(exchanges,now):
	"""Function to insert exchange information into securities master database"""
	
	for exchange in exchanges:
		print('Inserting row into Exchange Table')
		print(exchange)
		try:
			Exchange.create(abbrev=exchange['abbrev'],
					name =exchange['name'],
					city =exchange['city'],
					country=exchange['country'],
					currency=exchange['currency'],
					timezone_offset=exchange['timezone_offset'],
					created_date = now,
					last_updated_date=now)
		except:
			print('{} already exists'.format(exchange['abbrev']))
			exchange_record = Exchange.get(abbrev=exchange['abbrev'])
			print(exchange_record)
			exchange_record.name=exchange['name']
			exchange_record.city=exchange['city']
			exchange_record.currency=exchange['currency']
			exchange_record.time_zone_offset = exchange['timezone_offset']
			exchange_record.last_updated_date =now
			exchange_record.save()
			
def insert_data_vendor(data_vendors,now):
	"""Function to insert data vendor  information into securities master data base"""
	
	
	for data_vendor in data_vendors:
		try:
			print('Inserting row into Data Vendor Table')
			print(data_vendor)
			Data_Vendor.create(name=data_vendor['name'],
					website_url =data_vendor['website_url'] ,
					support_email =data_vendor['support_email'] ,
					created_date = now,
					last_updated_date=now)
		except:
		
	
			print('{} already exists'.format(data_vendor['name']))
			data_vendor_record = Data_Vendor.get(name=data_vendor['name'])
			print(data_vendor_record)
			data_vendor_record.website_url=data_vendor['website_url']
			data_vendor_record.support_email=data_vendor['support_email']
			data_vendor_record.last_updated_date =now
			data_vendor_record.save()

def insert_symbols(data_frame,now,exchange,instrument,currency):
	"""Function to take data frame and save it to securities master database"""
	
	# convert the data frame to a list of dictionaries
	symbols = data_frame.to_dict('records')
	print(str(symbols))	
	# get existing list of exchange abbreviation and asx code, test for duplicates
	existing_exchanges = Exchange.select()
	existing_exchange_list =  [existing_exchange.abbrev for existing_exchange in existing_exchanges]
	print(existing_exchange_list)
	
	existing_symbols= Symbol.select()		
	existing_symbol_list= [existing_symbol.ticker for existing_symbol in existing_symbols]
	print(existing_symbol_list)	


	for symbol in symbols:
		print(str(symbol))
		print(symbol['ASX code'])
		if symbol['ASX code'] in existing_symbol_list:		
			print('{} {} already exists'.format(exchange,symbol['ASX code']))
			symbol_record = Symbol.get(ticker=symbol['ASX code'])
			print(symbol_record)
			symbol_record.instrument=instrument
			symbol_record.name=name=symbol['Company name']
			symbol_record.sector=symbol['GICS industry group']
			symbol_record.currency=currency
			symbol_record.last_updated_date=now
			symbol_record.save()
			

		else:
			Symbol.create(exchange=Exchange.get(abbrev=exchange).id,
					ticker=symbol['ASX code'],
					instrument=instrument,
					name=symbol['Company name'],
					sector=symbol['GICS industry group'],
					currency=currency,
					created_date=now,
					last_updated_date=now)
		

	# first time - save all data
	
	# second time -if ntegrity error, only save update


if __name__=='__main__':
	asx_listing=open_ASX_listing_from_csv('asx_listing/ASXListedCompanies.csv')
	insert_exchange(exchange,now)
	insert_data_vendor(data_vendor,now)
	insert_symbols(asx_listing,now,'asx','equity','AUD')
