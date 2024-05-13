def iex_search_ticker(look_x_tickers = [""],tickers_df=None):
    """
    Returns a dataframe with the tickers that matches the user input.
    Parameters: 
    tickers_df: a dataframe with the tickers. If it is not provided, 
    the function will get one automatically through get_tickers_IEX().
    look_x_tickers: a list with the tickers to look for. It can handle
    also a single string with the tickers separated by spaces.
    """
    
    #checks wether a dataframe is provided. If not, it is downloaded trhouhg get_tickers_IEX()
    if tickers_df is None:
        
            print(f"No database was provided \nGetting data base from IEX...")
            tickers_df=get_tickers_IEX()
           
            if tickers_df is not None: print("Succesfully downloaded database.")
            else: return "Data base could not be downloaded. Please try again later."
                
    #if a string is provided as "look_x_tickers" parameter, then it splits the string by 
    #spaces and store the outcome in a list.
    if  type(look_x_tickers) is str:
        look_x_tickers = look_x_tickers.split(" ")
        
    #checks if an invalid argument is passed trhough "look_x_tickers" parameter such
    #as no argument at all or an empty list '[]'. If that's the case, it will return a
    #message explaining why the method won't go forward after this point.
    if (len(look_x_tickers) == 1 and look_x_tickers[0] == "") or look_x_tickers==[]:
            return "Must provide at least one character to look for the stock ticker in databse"
               
    #If the parameters provided are valid, then it will return a dataframe "search_results".
    else:
        
        #create an empty dataframe to store the results later
        search_results = pd.DataFrame()
        #loops through the list of tickers to look for
        for stock in look_x_tickers:

            #stores the reults for each ticker and store that result in "search_results"
            results_for_ticker = tickers_df[tickers_df["symbol"].str.startswith(stock)]
            search_results = pd.concat([search_results,results_for_ticker], axis=0)
            
        return search_results