import GraphPlotter

class backtester:
    def __init__(self ,symbols, df, strategy):
        self.symbols = symbols
        self.df = df
        self.strategy = strategy
        self.balance = 1000
        self.position_unit = 20
        self.balance_history = []
        self.amount_of_coins = {} #if equals 0 means no position, if positive means long position, if negative means short position
        self.coin_count_in_position = 0
        self.entry_price = {}
        self.tp_counter = {'long': {} , 'short': {}}
        self.sl_counter = {'long': {} , 'short': {}}
        self.exit_counter = {'long': {} , 'short': {}}

        for symbol in symbols:
            self.amount_of_coins[symbol] = 0
            self.entry_price[symbol] = 0
            self.tp_counter['long'][symbol] = 0; self.tp_counter['short'][symbol] = 0
            self.sl_counter['long'][symbol] = 0; self.sl_counter['short'][symbol] = 0
            self.exit_counter['long'][symbol] = 0; self.exit_counter['short'][symbol] = 0


    def do_backtest(self):
        for i in range(len(self.df['ohlcv-history'][self.symbols[0]]['close'])):
            for symbol in self.symbols:

                if self.check_position_side(symbol) == 'long':
                    if self.strategy.check_exit_long(symbol, i):
                        self.exit_long(symbol, i)
                    rType, oType, price = self.strategy.check_exit_long_tp_sl(symbol, i)
                    if rType:
                        self.exit_long_tp_sl(symbol, i , oType , price)    
                    

                if self.check_position_side(symbol) == 'short':
                    if self.strategy.check_exit_short(symbol, i):
                        self.exit_short(symbol, i)
                    rType, oType, price = self.strategy.check_exit_short_tp_sl(symbol, i)
                    if rType:
                        self.exit_short_tp_sl(symbol, i , oType , price)    

                if self.check_position_side(symbol) == 'no position' and self.balance > self.position_unit:
                    if self.strategy.check_enter_long(symbol, i):
                        self.enter_long(symbol, i)
                    elif self.strategy.check_enter_short(symbol, i):
                        self.enter_short(symbol, i)

            if(i%12 == 0):self.balance_history.append(self.balance + (self.coin_count_in_position*self.position_unit))

        self.print_results()
        

    def check_position_side(self, symbol):
        if self.amount_of_coins[symbol] == 0:
            return 'no position'
        elif self.amount_of_coins[symbol] > 0:
            return 'long'
        else:
            return 'short'
        

    def enter_long(self, symbol, i):
        self.amount_of_coins[symbol] = self.position_unit / self.df['ohlcv-history'][symbol]['close'][i]
        self.balance -= self.position_unit
        self.coin_count_in_position += 1
        self.entry_price[symbol] = self.df['ohlcv-history'][symbol]['close'][i]
        self.print_operations(symbol , i , 'Enter Long')

    def enter_short(self, symbol, i):
        self.amount_of_coins[symbol] = -self.position_unit / self.df['ohlcv-history'][symbol]['close'][i]
        self.balance -= self.position_unit
        self.coin_count_in_position += 1
        self.entry_price[symbol] = self.df['ohlcv-history'][symbol]['close'][i]
        self.print_operations(symbol , i , 'Enter Short')

    def exit_long(self, symbol, i):
        self.balance += self.amount_of_coins[symbol] * self.df['ohlcv-history'][symbol]['close'][i]
        self.amount_of_coins[symbol] = 0
        self.coin_count_in_position -= 1
        difference = self.df['ohlcv-history'][symbol]['close'][i] - self.entry_price[symbol]
        self.entry_price[symbol] = 0
        #self.print_operations(symbol , i , 'Exit Long' , difference)

    def exit_short(self, symbol, i):
        self.balance += (self.position_unit*2)-(-self.amount_of_coins[symbol] * self.df['ohlcv-history'][symbol]['close'][i])
        self.amount_of_coins[symbol] = 0
        self.coin_count_in_position -= 1
        difference = self.df['ohlcv-history'][symbol]['close'][i] - self.entry_price[symbol]
        self.entry_price[symbol] = 0
        #self.print_operations(symbol , i , 'Exit Short' , difference)   

    def exit_long_tp_sl(self, symbol, i , oType , price):
        self.balance += self.amount_of_coins[symbol] * price
        self.amount_of_coins[symbol] = 0
        self.coin_count_in_position -= 1
        difference = price - self.entry_price[symbol]
        self.entry_price[symbol] = 0
        if oType == 'tp':
            self.tp_counter['long'][symbol] += 1
            self.print_operations(symbol , i , 'Long TP' , difference)
        elif oType == 'sl':
            self.sl_counter['long'][symbol] += 1
            self.print_operations(symbol , i , 'Long SL' , difference)

    def exit_short_tp_sl(self, symbol, i , oType , price):
        self.balance += (self.position_unit*2)-(-self.amount_of_coins[symbol] * price)
        self.amount_of_coins[symbol] = 0
        self.coin_count_in_position -= 1
        difference = price - self.entry_price[symbol]
        self.entry_price[symbol] = 0
        if oType == 'tp':
            self.tp_counter['short'][symbol] += 1
            self.print_operations(symbol , i , 'Short TP' , difference)
        elif oType == 'sl':
            self.sl_counter['short'][symbol] += 1
            self.print_operations(symbol , i , 'Short SL' , difference)

        
    def print_operations(self , symbol , i , operation_name , difference=0):

        print(symbol , " " , operation_name)
        if difference != 0: print('Difference: ', difference)
        print('Close price: ', self.df['ohlcv-history'][symbol]['close'][i])
        print('Time: ', self.df['ohlcv-history'][symbol]['time'][i])
        print('Balance: ', self.balance)
        print('Amount of coins: ', self.amount_of_coins[symbol])
        print('Coin count in position: ', self.coin_count_in_position)
        print("----------------------------------------------------")
        
        
    def print_results(self):

        for symbol in self.symbols:
            
            print('Symbol: ', symbol)
            print('Amount of coins: ', self.amount_of_coins[symbol])
            print('Long TP Counter: ', self.tp_counter['long'][symbol] , ' Short TP Counter: ', self.tp_counter['short'][symbol])
            print('Long SL Counter: ', self.sl_counter['long'][symbol] , ' Short SL Counter: ', self.sl_counter['short'][symbol])
            print('Long Exit Counter: ', self.exit_counter['long'][symbol] , ' Short Exit Counter: ', self.exit_counter['short'][symbol])
            print("----------------------------------------------------")    

        print('Balance: ', self.balance)
        print('Coin count in position: ', self.coin_count_in_position)
        graph = GraphPlotter.draw(self.balance_history , 'Balance History')