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

print(group_df.head())
print(group_df.tail())
