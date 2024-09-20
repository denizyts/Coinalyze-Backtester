# Futures Backtester for financial markets.

This project allows you to test your strategies on historical Open interest , Long short ratio , 
OHLCV , Liquidation datas. fetched from coinalyze.net 

##https://coinalyze.net

If you have any problem send mail to me by using the adress on my profile
*https://github.com/denizyts*

## Table of Contents

- [Why Should I Use This Backtester](#Why)
- [Details](#Details)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Why Should I Use This Backtester ?
-This Script allows to do testing on csv files fetched from coianlyze api.
  
-High flexibility, by adding few lines of code you can make big changes.

-Multiple Intervals, you can do backtest at 15 min timeframe but same time you can check the data on 1 hour timeframe.

-Allows multiple assets, you can test your strategies with several assets.

## Details

### Historical Data
The csv files are fetched from the coinalyze.net api please check https://api.coinalyze.net/v1/doc/ for more information.

### Multiple Timeframes
At *main.py* initially there are 4 timeframes those are 15m , 1h , 4h , 1d. Those historical datas fetched already, Strategies are very flexible with this multiple timeframes.
Also you can add more timeframes, but backtest are done at smallest interval , it means the main loop has length of the smallest period csv.

### Assets
*symbols.txt* files are store asset names of coins, at the design those are like *BTCUSDT_PERP.A* *SOLUSDT_PERP.A*. 
! Please delete empty lines on symbols.txt files. !

### Indicators
At *strategy.py* indicators are from pandas_ta, easy and fast to use for more information:
*https://github.com/twopirllc/pandas-ta*

Also there are vwapCalcV2 which implemented by me. You can check it:
*https://github.com/denizyts/vwapCalc*

### Write Data into a CSV
On main set the names then call the *fetch_writer.fetch_write()* there are command lines shows how to call it.

### TPSL & Exit
Backtester class includes many options for your strategy thoose are Take Profit , Stop Loss and Exits , Thoose methods can be combined or can be used indivudally, set TP and SL levels 
You can change the returns(Boolean) of the close_long and close_short methods in *strategy.py* .

### Final log outputs
Those outputs show the long/short close/tp/sl counter for each asset. Also shows Last balance , total operation counter. 
Those last outputs are very vital for real algo traders.

# Installation

Clone the repository with git:

*git clone https://github.com/denizyts/Coinalyze-Backtester.git*

or just download the zip.

## Dependencies
Latest versions probably will be enough.

- *Python 3.11.8*
- *pandas 2.1.2*
- *pandas_ta 0.3.14*
- *numpy 1.26.0*
- *matplotlib 3.8.0*

## Usage
*-python3 main.py*







