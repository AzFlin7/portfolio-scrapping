def get_assets_hist_data(tickers_dict={"index":[],"crypto":[]}, years=2):
    
    #Defining starting dat to get historical data.
    data_start_date = datetime.now() + timedelta(int(-365*years))

    #getting indeces historical prices form IEX
    portfolio_hist_prices = mc.get_historic_data(ticker = tickers_dict["index"], 
                                                 start_date = data_start_date)

    #getting cryptos historical prices form cryptocompare
    btc_daily_price = mc.get_crypto_daily_price(tickers_dict["crypto"],limit=int(years*365))

    #concatenating both dataframes
    portfolio_hist_prices = pd.concat([portfolio_hist_prices,btc_daily_price],axis=1,join="inner")
    portfolio_hist_prices.dropna(inplace=True)
    portfolio_hist_prices = portfolio_hist_prices[(portfolio_hist_prices[portfolio_hist_prices.columns] != 0).all(axis=1)]

    #formating dataframes
    portfolio_hist_prices = mc.normalize_dataframe(portfolio_hist_prices)
    portfolio_daily_retn = portfolio_hist_prices.pct_change().copy()
    
    #Save both hist. prices and hist. daily returns dataframes packed in a list to be able to return in the funtion.
    hist_price_ret_df = [ portfolio_hist_prices, portfolio_daily_retn ]
    
    return hist_price_ret_df