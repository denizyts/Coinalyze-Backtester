import fetch_write
from datetime import datetime
import pandas as pd
import control_csv_fitting
import GraphPlotter 
from strategy import Strategy
from strategy2 import Strategy2
from backtester import backtester
import txtReader


from_date = datetime(2024, 9, 14 )
to_date = datetime(2024, 9, 19 )
symbols = ['BTCUSDT_PERP.A', 'ETHUSDT_PERP.A' , 'SOLUSDT_PERP.A']
symbols = ['ETHUSDT_PERP.A']
symbols = txtReader.reader()
interval = '5min'

#dont use liq history because coinalyze has issues with it.
data_types = ['long-short-ratio-history' , 'open-interest-history' , 'liquidation-history' ,'ohlcv-history']
data_types = ['long-short-ratio-history' , 'open-interest-history' , 'ohlcv-history']

titles_long_short_ratio_history = ['time' , 'ratio' , 'long' , 'short']
titles_open_interest_history = ['time' , 'open' , 'high' , 'low' , 'close']
titles_liquidation_history = ['time' , 'liquidation_long' , 'liquidation_short']
titles_ohlcv_history = ['time' , 'open' , 'high' , 'low' , 'close' , 'volume' , 'bv' , 'tx' , 'btx'] 

titles = {
    'long-short-ratio-history': ['time', 'ratio', 'long', 'short'],
    'open-interest-history': ['time', 'open', 'high', 'low', 'close'],
    'liquidation-history': ['time', 'liquidation_long', 'liquidation_short'],
    'ohlcv-history': ['time', 'open', 'high', 'low', 'close', 'volume', 'bv', 'tx', 'btx']
}


df = {
    'long-short-ratio-history': {},
    'open-interest-history': {},
    'liquidation-history': {},
    'ohlcv-history': {}
}


def write_symbols_all_datas(from_date, to_date, symbol, interval, data_types):
 for symbol in symbols:
    for data_type in data_types:
     print(data_type)
     fetch_write.fetch_write_data(from_date, to_date, symbol, interval, data_type)
    

write_symbols_all_datas(from_date, to_date, symbols, interval, data_types)

#checks if the lengths of the dataframes are equal
prev_length = 0; length = 0; counter = 0
for symbol in symbols:
    for data_type in data_types:
        folder = r"your folder path"
        name = f'{symbol}_{data_type}.csv'
        df[data_type][symbol] = pd.read_csv(folder+name, names=titles[data_type])
        prev_length = length
        length = len(df[data_type][symbol]['time'])
        if prev_length != length and counter != 0:
            print(f'{symbol} - {data_type} - {length} rows')
        counter += 1    


#control_csv_fitting.control(df)


strategy = Strategy2(symbols , df)
backtester = backtester( symbols , df , strategy)

backtester.do_backtest()


