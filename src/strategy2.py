import pandas_ta 
import GraphPlotter


class Strategy2:

    def __init__(self, symbols , df):
        self.symbols = symbols
        self.df = df
        
        self.long_short_ratio_data_rsi = {}
        self.oi_data_rsi = {}
        self.oi_data_zscore = {}
        self.close_rsi = {}
        self.close_zscore = {}
        self.close_ema = {}

        self.tp_perc = 1.025
        self.sl_perc = 0.9875
        self.tp_perc_short = 1-(self.tp_perc-1)
        self.sl_perc_short = 1+(1-self.sl_perc)
        self.entry_price = {}

        self.mode = 'tp_sl' # tp_sl or exit

        for symbol in self.symbols:

            self.long_short_ratio_data_rsi[symbol] = pandas_ta.rsi(df['long-short-ratio-history'][symbol]['ratio'], length=14)  
            self.oi_data_rsi[symbol] = pandas_ta.rsi(df['open-interest-history'][symbol]['close'], length=14)
            self.oi_data_zscore[symbol] = pandas_ta.zscore(df['open-interest-history'][symbol]['close'], length=14)
            
            self.close_rsi[symbol] = pandas_ta.rsi(df['ohlcv-history'][symbol]['close'], length=14)
            self.close_zscore[symbol] = pandas_ta.zscore(df['ohlcv-history'][symbol]['close'], length=14)
            self.close_ema[symbol] = pandas_ta.ema(df['ohlcv-history'][symbol]['close'], length=35)
            
        #GraphPlotter.draw(self.long_short_ratio_data_rsi['BTCUSDT_PERP.A'] , 'BTCUSDT_PERP.A - Long Short Ratio RSI')   
        #GraphPlotter.draw(self.oi_data_rsi['BTCUSDT_PERP.A'] , 'BTCUSDT_PERP.A - Open Interest RSI') 
        #GraphPlotter.draw(df['open-interest-history']['BTCUSDT_PERP.A']['close'] , 'BTCUSDT_PERP.A - Open Interest')

        print('Strategy initialized')

    def check_enter_long(self , symbol , i):
        
        if i == 0: return False

        condition1 = self.close_rsi[symbol][i] < 35
        condition2 = self.close_zscore[symbol][i-1] < -1.5 and self.close_zscore[symbol][i] > self.close_zscore[symbol][i-1]
        condition3 = self.check_candle_color(self.df['open-interest-history'][symbol] , i) == 'green' 
        condition4 = self.oi_data_rsi[symbol][i] < 35

        if condition1 and condition2 and condition3 and condition4:
            self.entry_price[symbol] = self.df['ohlcv-history'][symbol]['close'][i]
            return True
            
    def check_enter_short(self , symbol , i):

        if i == 0: return False
        
        condition1 = self.close_rsi[symbol][i] > 65
        condition2 = self.close_zscore[symbol][i-1] > 1.5 and self.close_zscore[symbol][i] < self.close_zscore[symbol][i-1]
        condition3 = self.check_candle_color(self.df['open-interest-history'][symbol] , i) == 'green'
        condition4 = self.oi_data_rsi[symbol][i] < 35
        
        if condition1 and condition2 and condition3 and condition4:
            self.entry_price[symbol] = self.df['ohlcv-history'][symbol]['close'][i]
            return True
    
    def check_exit_long(self , symbol , i):
        if self.mode != 'exit':
            return False
        
        return True
    
    def check_exit_short(self , symbol , i):
        if self.mode != 'exit':
            return False
        
        return True
            
    def check_exit_long_tp_sl(self , symbol , i):
        
        if self.mode != 'tp_sl':
            return False , '' , 0

        tpPrice = self.entry_price[symbol] * self.tp_perc
        slPrice = self.entry_price[symbol] * self.sl_perc

        if tpPrice < self.df['ohlcv-history'][symbol]['high'][i]:
            return True , 'tp' , tpPrice
        if slPrice > self.df['ohlcv-history'][symbol]['low'][i]:
            return True , 'sl' , slPrice
        else:
            return False , '' , 0
        
    def check_exit_short_tp_sl(self , symbol , i):

        if self.mode != 'tp_sl':
            return False , '' , 0

        tpPrice = self.entry_price[symbol] * self.tp_perc_short
        slPrice = self.entry_price[symbol] * self.sl_perc_short
        
        if tpPrice > self.df['ohlcv-history'][symbol]['low'][i]:
            return True , 'tp' , tpPrice
        if slPrice < self.df['ohlcv-history'][symbol]['high'][i]:
            return True , 'sl' , slPrice
        else:
            return False , '' , 0
        

    def check_candle_color(self , data , i):
        if data['close'][i] > data['open'][i]:
            return 'green'
        else:
            return 'red'