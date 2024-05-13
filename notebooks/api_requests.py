import pandas as pd
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import json
import os

def read_json(url):
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    url2 = json.loads(data)
    return url2

api_key = os.getenv("CC_API")
ticker_list = ['BTC', 'LTC', 'ETH', 'ZEC', 'XRP']
group_df = pd.DataFrame()

for ticker in ticker_list:
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={ticker}&tsym=USD&allData=true&api_key={api_key}"
    raw_data = read_json(url)
    df = pd.DataFrame(raw_data['Data']['Data'])
    df['time'] = pd.to_datetime(df['time'],unit='s')
    df.set_index(df['time'], inplace=True)
    df['close'] = df['close'].astype(float)
    group_df[ticker] = df['close']

sp500_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=VOO&outputsize=full&apikey=HR2ZZ9PKUC9R8DFL"
sp500_raw = read_json(sp500_url)

date, close = [],[]
for x, y in sp500_raw["Time Series (Daily)"].items():
    close.append(float(y['4. close']))
    date.append(x)
sp500_df = pd.DataFrame(close, index = date).sort_index(ascending=True)

sp500_df.reset_index(inplace = True)
sp500_df['index'] = pd.to_datetime(sp500_df['index'])
sp500_df = sp500_df.rename(columns = {'index':'time'})
sp500_df.set_index(sp500_df['time'], inplace=True)
sp500_df.drop(columns=['time'], inplace = True)
sp500_df = sp500_df.rename(columns={0:'sp500'})

joint_df = pd.concat([group_df, sp500_df], axis=1, join='inner')

---
#Version 2 calling all info from 1 API
import pandas as pd
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import json
import os

def read_json(url):
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    url2 = json.loads(data)
    return url2

def get_crypto():
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market=USD&apikey={api_key}"
    raw_data = read_json(url)
    raw_df = pd.DataFrame(raw_data['Time Series (Digital Currency Daily)']).T
    group_df[ticker] = raw_df['4a. close (USD)'].astype(float)
    
def get_stock():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={api_key}"
    raw_data = read_json(url)
    raw_df = pd.DataFrame(raw_data['Time Series (Daily)']).T
    group_df[ticker] = raw_df['4. close'].astype(float)


api_key = 'HR2ZZ9PKUC9R8DFL'
ticker_list = ['BTC', 'LTC', 'ETH', 'ZEC', 'XRP', 'VOO']
stock_list = ['VOO']
group_df = pd.DataFrame()


for ticker in ticker_list:
    if ticker in stock_list:
        get_stock() 
    else:
        get_crypto()

        
group_df.sort_index(inplace=True)