def normalize_dataframe(df=None):
    """
    Returns a dataframe with the normalize format for this library.
    The normalize format is a dataframe with only the close values of the ticker with the 
    columns named as the ticker. 
    Accepts dataframes with columns that are 2-level indexed where the upper index contains
    the ticker and the lower has at least one column named "close".
    """
    #Drops all the columns that are not 'close'
    col_to_drop = df.columns.levels[1].values
    col_to_drop = np.delete(col_to_drop,np.where(col_to_drop=="close"))
    df = df.drop(columns=col_to_drop, level=1)
    #eliminates the double level in columns by deleting the 'close' label. 
    #Only ticker label is necessary.
    df.columns = df.columns.droplevel(1)
    return df