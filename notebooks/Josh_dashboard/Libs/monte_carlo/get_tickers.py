def get_tickers_IEX():
    """
    Returns a dataframe with all the tickers available in IEX Cloud.
    token is stored in environment key IEX_TOKEN as sugested by IEX. 
    In this was, it is not necessary to call os.getenv() function
    """
    #iex_token = os.getenv("IEX_PUBLIC_KEY")
    
   # if type(iex_token) == str: print("IEX Key found successfully ...getting data")
   # else: return "Error: IEX Key NOT found"
    
    tickers=pd.DataFrame(get_symbols(output_format='pandas',
                                     #token=iex_token
                                    ))
    return tickers