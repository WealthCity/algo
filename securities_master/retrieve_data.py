from .securities_master import Exchange, Data_Vendor, Symbol, Daily_Price
import pandas as pd
from datetime import datetime

def get_data_from_ticker(ticker, start_date=None, end_date=None):
	"""Function that takes a ticker symbol and returns a data frame with the data"""	
	# check to see if the symbol is in the database
	existing_symbols = Symbol.select()
	existing_symbol_list = [existing_symbol.ticker for existing_symbol in existing_symbols]
	
	if ticker in existing_symbol_list:
		symbol_record = Symbol.get(ticker=ticker)	
		print(symbol_record.ticker)
		symbol_id = symbol_record.id
		print(symbol_id)			
		existing_price_data=None	
		#print(len(start_date))
		#print(len(end_date))	
		
		if start_date is not None:
			if end_date is not None:
				existing_price_data = Daily_Price.select().where((Daily_Price.symbol==symbol_id) & (Daily_Price.price_date>=start_date) & (Daily_Price.price_date<=end_date)).dicts()	
		

	
		if start_date is None and end_date is None:
			existing_price_data = Daily_Price.select().where(Daily_Price.symbol==symbol_id).dicts()	
			print(existing_price_data)		
	# if start date is none, select the earliest entry
		
		if start_date is not None and end_date is None:	
			existing_price_data = Daily_Price.select().where((Daily_Price.symbol==symbol_id) & (Daily_Price.price_date>= start_date)).dicts()	
			print(existing_price_data)

	# if end date is non, select the latest entry
		if start_date is None and end_date is not None:	
			existing_price_data = Daily_Price.select().where((Daily_Price.symbol==symbol_id) & (Daily_Price.price_date<= end_date)).dicts()	
			print(existing_price_data)

			
					
	#	if start_date is not None and end_date is None:
#			print(datetime.strptime(start_date,'%Y-%m-%d'))
	#		existing_price_data = Daily_Price.select().where(Daily_Price.symbol==symbol_id)
	#		print(existing_price_data)
	#		existing_price_data = Daily_Price.select().where(Daily_Price.price_date>=datetime.strptime(start_date,'%Y-%m-%d')).dicts()
			#existing_price_data=existing_price_data.dicts()		
	#		print(existing_price_data)	
		
		#if start_date is not None or end_date is not None:
			
		#	existing_price_data = Daily_Price.select().where((Daily_Price.symbol==symbol_id) and(Daily_Price.price_date>=start_date) and (Daily_Price.price_date<=end_date)).dicts()	
			
	# return data frame
		
		existing_price_data_frame=pd.DataFrame.from_records(existing_price_data)
		del existing_price_data
		existing_price_data_frame=existing_price_data_frame.set_index('price_date')
		print(existing_price_data_frame.head())
		print(existing_price_data_frame.tail())
		return(existing_price_data_frame)
	else:
		print('Symbol was not found in database')	
		return(None)

if __name__ == '__main__':
	data = get_data_from_ticker('1PG')			
	data = get_data_from_ticker('1PG',start_date='2008-07-01')
	data = get_data_from_ticker('1PG',end_date='2015-07-30')
	data = get_data_from_ticker('1PG',start_date='2015-07-01',end_date='2015-07-30')
