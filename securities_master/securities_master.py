import peewee
from peewee import *
import pandas as pd


db = peewee.MySQLDatabase('securities_master',user = 'sec_user', passwd='password')

class BaseModel(Model):
	class Meta:
		database =db

class Exchange(BaseModel):
	#exchange_id = IntegerField(primary_key = True,unique = True,null=False)
	abbrev = CharField(null=False,max_length=32,unique=True)
	name = CharField(null=False,max_length=255) 
	city =CharField(null=True,max_length=255) 
	country =CharField(null=True,max_length=255) 
	currency = CharField(null=True,max_length=64) 
	timezone_offset = TimeField()
	created_date =  DateTimeField(null=False)
	last_updated_date =  DateTimeField(null=False)

	
class Data_Vendor(BaseModel):
	#data_vendor_id =IntegerField(primary_key = True,unique = True,null=False) 
	name = CharField(null=False,max_length=64,unique=True) 
	website_url= CharField(null=True,max_length=255) 
	support_email = CharField(null=True,max_length=255) 
	created_date = DateTimeField(null=False) 
	last_updated_date = DateTimeField(null=False) 
 
		

class Symbol(BaseModel):
	#symbol_id =IntegerField(primary_key = True,unique = True,null=False) 
	exchange =ForeignKeyField(Exchange)
	ticker = CharField(null=False,max_length=32) 
	instrument = CharField(null=False,max_length=64) 
	name = CharField(null=True,max_length=255) 
	sector = CharField(null=True,max_length=255) 
	currency = CharField(null=True,max_length=32) 
	created_date = DateTimeField(null=False)
	last_updated_date = DateTimeField(null=False)


class Daily_Price(BaseModel):
	#daily_price_id =IntegerField(primary_key = True,unique = True,null=False) 
	data_vendor = ForeignKeyField(Data_Vendor)
	symbol = ForeignKeyField(Symbol)
	price_date = DateTimeField(null=False)
	created_date = DateTimeField(null=False)
	last_updated_date = DateTimeField(null=False)
	open_price = DecimalField(null=True,decimal_places=4) 
	high_price = DecimalField(null=True,decimal_places=4)
	low_price = DecimalField(null=True,decimal_places=4)
	close_price = DecimalField(null=True,decimal_places=4)
	adj_close_price = DecimalField(null=True,decimal_places=4)
	volume = BigIntegerField()

if __name__=='__main__':
	db.connect()
	#db.drop_table([Exchange,Data_Vendor,Symbol,Daily_Price])
	db.create_tables([Exchange,Data_Vendor,Symbol,Daily_Price],safe = True)
