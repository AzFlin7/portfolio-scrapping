def get_crypto_daily_price(cryptotickers = [], allData=False,limit = 90):
    """
    Returns a dataframe with the close prices of the cryptocurrencies selected. 
    Arguments:
    cryptotickers: list of tickers for currencies.
    allData: if True, gets all historical data available and ignores argument "limit".
    By default it is False.
    limit: the days from now to get the historical data. By default it's 90.
    """
    api_key = os.getenv("CC_API")
    ticker_list = cryptotickers
    crypto_df = pd.DataFrame()

    for ticker in ticker_list:
        #if allData is true, then it gets all the data available. If not, select data according to limit.
        if allData:
            url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={ticker}&tsym=USD&allData=true&api_key={api_key}"
        else:
            url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={ticker}&tsym=USD&limit={limit}&api_key={api_key}"
       
        raw_data = read_json(url)
        #print(json.dumps(raw_data, indent=5))
        df = pd.DataFrame(raw_data['Data']['Data'])
        df['time'] = pd.to_datetime(df['time'],unit='s')
        df.set_index(df['time'], inplace=True)
        df['close'] = df['close'].astype(float)
        crypto_df[ticker] = df['close']
    
    #
    new_columns = pd.MultiIndex.from_product([ crypto_df.columns, ["close"]  ])
    crypto_df.columns = new_columns

    return crypto_df