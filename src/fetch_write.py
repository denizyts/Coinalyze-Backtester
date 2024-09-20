import requests
from datetime import datetime, timezone, timedelta
import csv
from config import api_key


def unixconverter(data):

    tz_offset = timedelta(hours=3)
    
    for i in range(len(data[0]['history'])):
        print(data[0]['history'][i]['t']); print("index" , i)
        data[0]['history'][i]['t'] = (int(data[0]['history'][i]['t']))
        utc_time = datetime.fromtimestamp(data[0]['history'][i]['t'] )
        local_time = utc_time + tz_offset
        data[0]['history'][i]['t'] = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return data  

def unixconverterV2(data):
    tz_offset = timedelta(hours=0)
    
    for i in range(len(data[0]['history'])):
        t_value = data[0]['history'][i]['t']
        
        if isinstance(t_value, int):  # If it's a Unix timestamp
            utc_time = datetime.fromtimestamp(t_value)
            local_time = utc_time + tz_offset
            data[0]['history'][i]['t'] = local_time.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(t_value, str):  # If it's already a string, just keep it
            try:
                datetime.strptime(t_value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"Unexpected date format: {t_value}")
                raise
    return data  


def check_fix_missed_rows(data):
    for i in range(len(data[0]['history']) - 1):
        if (data[0]['history'][i]['t']) + 300 != (data[0]['history'][i+1]['t']):
            print('Missing row at index: ', i , ' Time: ' , data[0]['history'][i]['t'])
            row = data[0]['history'][i]
            row['t'] = (data[0]['history'][i]['t']) + 300
            data[0]['history'].insert(i+1, row)
    return data        
            

def write_Data(name , candles):
  
  folder = r"your_folder_path"
  extension = name 
  csvFile = open(folder+extension ,'w',newline = '')
  printer = csv.writer(csvFile,delimiter = ',')
    
    #WITH THIS FOR LOOP EACH ELEMENT OF CANDLE LIST WRITTEN ON ONLY ONE LINE SO ON CSV FILE THERE ARE NO LIST, LINES EXIST ONLY !
  for candle in candles:
   printer.writerow(candle.values())    
  csvFile.close()
  print('Data written successfully ' , name)

def fetch_write_data(from_date, to_date, symbol, interval, data_type):
    # Set your API key and endpoint (example values)
    api_key = config.api_key
    endpoint = 'https://api.coinalyze.net/v1/long-short-ratio-history'
    endpoint2 = 'https://api.coinalyze.net/v1/ohlcv-history'
    exchange_endpoint = 'https://api.coinalyze.net/v1/exchanges'
    param_endpoint = 'https://api.coinalyze.net/v1/' + f'{data_type}'

    from_timestamp = int(from_date.timestamp())
    to_timestamp = int(to_date.timestamp())

    symbol = symbol; interval = interval; data_type = data_type

    params = {
        'symbols': f'{symbol}',  
        'interval': f'{interval}',    
        'from': f'{from_timestamp}',  # Example start time (UNIX timestamp)
        'to': f'{to_timestamp}' ,    # Example end time (UNIX timestamp)
    }

    headers = {
        'api_key': f'{api_key}'
    }

    response = requests.get(param_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        print("Success")
        data = response.json()
        if data == []: print('DATA IS EMPTY !!!!!!!!!!!!!!!!!!!')
        print(from_date , to_date , symbol , interval , data_type)
        #print(data)
        data = check_fix_missed_rows(data)
        data = unixconverterV2(data)
        name = f'{symbol}_{data_type}.csv'
        write_Data(name, data[0]['history'])
        print(f"Data for {symbol} has been fetched and written to {symbol}_{data_type}.csv")
        #print(data)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    from_date = datetime(2023, 8, 12)
    to_date = datetime(2024, 8, 16)
    symbol = 'BTCUSDT_PERP.A'
    interval = '1hour'
    data_type = 'ohlcv-history'
    fetch_write_data(from_date, to_date, symbol, interval, data_type)  
    