

# CHECKS FOR TIME FITTING.


def control(df):

    btc_key = 'BTCUSDT_PERP.A'

    helper = 0;

    for i in range(len(df['ohlcv-history'][btc_key]['close'])):
        
        if df['ohlcv-history'][btc_key]['time'][i] == df['long-short-ratio-history'][btc_key]['time'][i]:
            print('Times are equal')
            helper += 1
        else:
            print('Times are not equal !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(df['ohlcv-history'][btc_key]['time'][i])
            return;
            

