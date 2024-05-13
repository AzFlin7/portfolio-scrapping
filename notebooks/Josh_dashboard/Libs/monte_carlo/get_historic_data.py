def get_historic_data(end_date = datetime.now(), 
                      start_date = datetime.now() + timedelta(-365),
                      ticker=[],
                      close_only=True):
    """
    Returns a data frame with the HOLC and Volume info from the for "ticker" 
    provided list. The info is provided by IEX Cloud.
    
    Parameters:
    end_date: The final date for the historic data. By default, it's today.
    start_date: The starting date for the historic data. By default, it's today a year ago.
    Example: datetime.now() + timedelta(-365). "This is a year ago".
    ticker: the list of the tickers of the stocks that is attemped to get the historic data.
    e.g. ticker =["AAPL","GOOG","SQ"]
    Also accepts a single string with the the list of tickers separated by spaces. 
    e.g. "AAPL GOOG SQ"
    close_only: Boolean. If False, it will return HOLC and volume values. If True, it will 
    return only closing and volume data for the tickers. By default, it is True for efficiency.
    """
    #checks if the parameters provided through "ticker" is not an empty list
    #if it is, the function won't go forward after this point. returns explanatory message.
    if ticker == []:
        return "Empty list of tickers"
    
    #if a string is provided as "ticker" parameter, then it splits the string by 
    #spaces and store the outcome in a list.
    elif type(ticker) is str:
        ticker = ticker.split(" ")
            
    #iex_token = os.getenv("IEX_PUBLIC_KEY")#not necessary anymore.
    
    #Gets historical data with the parameters provided.
    #Gets only "close" and "volume" value for efficiency.
    prices = get_historical_data(ticker, start_date, end_date,
                                 output_format='pandas', 
                                 #token=iex_token, 
                                 close_only=close_only
                                )
    
    #If only one ticker is provided, then it adds another indexing level to the column
    #with the ticker. This is done for two reasons: 1) To visualize the ticker downloaded  
    #as a confirmation that I am working with correct data. 2) To mimic the format of the
    #dataframe obtained when getting 2 or more tickers data (2-level column indexing).
    if len(ticker) == 1:
        new_columns = pd.MultiIndex.from_product([ [ticker[0]],prices.columns ] )
        prices.columns = new_columns
        
    return prices