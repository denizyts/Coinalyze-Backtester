import pandas_ta 
import GraphPlotter


class Strategy:

    def __init__(self, symbols , df):
        self.symbols = symbols
        self.df = df
        
        self.long_short_ratio_data_rsi = {}
        self.oi_data_rsi = {}
        self.liq_long_data_rsi = {}
        self.liq_short_data_rsi = {}
        self.close_rsi = {}
        self.close_zscore = {}
        self.close_ema = {}

        self.tp_perc = 1.05
        self.sl_perc = 0.975
        self.tp_perc_short = 1-(self.tp_perc-1)
        self.sl_perc_short = 1+(1-self.sl_perc)
        self.entry_price = {}

        self.mode = 'tp_sl' # tp_sl or exit

        for symbol in self.symbols:

            self.long_short_ratio_data_rsi[symbol] = pandas_ta.rsi(df['long-short-ratio-history'][symbol]['ratio'], length=14)  
            self.oi_data_rsi[symbol] = pandas_ta.rsi(df['open-interest-history'][symbol]['close'], length=14)
            self.liq_long_data_rsi[symbol] = pandas_ta.rsi(df['liquidation-history'][symbol]['liquidation_long'], length=14)
            self.liq_short_data_rsi[symbol] = pandas_ta.rsi(df['liquidation-history'][symbol]['liquidation_short'], length=14)

            self.close_rsi[symbol] = pandas_ta.rsi(df['ohlcv-history'][symbol]['close'], length=24)
            self.close_zscore[symbol] = pandas_ta.zscore(df['ohlcv-history'][symbol]['close'], length=14)
            self.close_ema[symbol] = pandas_ta.ema(df['ohlcv-history'][symbol]['close'], length=35)
            
        #GraphPlotter.draw(self.long_short_ratio_data_rsi['BTCUSDT_PERP.A'] , 'BTCUSDT_PERP.A - Long Short Ratio RSI')   
        #GraphPlotter.draw(self.oi_data_rsi['BTCUSDT_PERP.A'] , 'BTCUSDT_PERP.A - Open Interest RSI') 
        #GraphPlotter.draw(self.liq_data_rsi['BTCUSDT_PERP.A'] , 'BTCUSDT_PERP.A - Liquidation RSI')
        #GraphPlotter.draw(df['liquidation-history']['BTCUSDT_PERP.A']['liquidation_long'] , 'BTCUSDT_PERP.A - Liquidation Long')
        #GraphPlotter.draw(df['open-interest-history']['BTCUSDT_PERP.A']['close'] , 'BTCUSDT_PERP.A - Open Interest')

        print('Strategy initialized')

    def check_enter_long(self , symbol , i):
        
        condition1 = self.liq_long_data_rsi[symbol][i] > 75
        condition2 = self.oi_data_rsi[symbol][i] < 50
        
        technical_condition = self.close_rsi[symbol][i] < 35 
        
        if condition1 and condition2 and technical_condition:
            self.entry_price[symbol] = self.df['ohlcv-history'][symbol]['close'][i]
            return True
            
    def check_enter_short(self , symbol , i):
        
        condition1 = self.liq_short_data_rsi[symbol][i] > 75
        condition2 = self.oi_data_rsi[symbol][i] < 50

        technical_condition = self.close_rsi[symbol][i] > 65 
        
        if condition1 and condition2 and technical_condition:
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
        