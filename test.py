import securities_master.retrieve_data as rd
#from time_series_analysis.test_stationarity import Test_Stationarity
#from cointegration.cointegration import plot_price_series
#from cointegration.cointegration import plot_scatter_series
from cointegration.cointegration import cointegrate
import forecast.forecast as f
import performance_management.performance_management as pm 
import risk_management.risk_management as rm
data1 = rd.get_data_from_ticker('CBA')
data2= rd.get_data_from_ticker('WBC')

#test = Test_Stationarity(data,'close_price')
#print(str(test.series))
#test.dickey_fuller_test()
#test.test_hurst_exponent()

#plot_price_series(data1,'close_price',data2,'close_price')
#plot_scatter_series(data1,'close_price',data2,'close_price')
#cointegrate('1PG',data1,'close_price','CBA',data2,'close_price')
#lagged_time_series = f.create_lagged_series(data1,'close_price',lags=2)

#print(pm.annualised_sharpe(data1,'close_price'))
#print(pm.equity_sharpe(data1,'close_price'))
#print(pm.market_neutral_sharpe(data1,'close_price',data2,'close_price'))

print(rm.var_cov_var(70000,data1,'close_price'))
#print(lagged_time_series)

#f.forecast(lagged_time_series,['Today','Lag_1%','Lag_2%'],'Direction',0.7,0.3)



