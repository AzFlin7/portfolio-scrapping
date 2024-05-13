######Portfolio Standard Deviation Start
from pandas_datareader import data as web
import pandas as pd
import numpy as np

#trial data to be replaced by portfolio intruments' daily returns DataFrame
assets =  ['QQQ', 'WMT', 'VOO', 'AMD', 'NVDA'] 

df = pd.DataFrame()  

for stock in assets:
    df[stock] = web.DataReader(stock, data_source='yahoo',
                               start='2018-1-1' , end='2019-1-1')['Adj Close']

daily_returns = df.pct_change()  
#End trial data

cov_matrix_d = daily_returns.cov()
cov_matrix_a = cov_matrix_d * 252

#Option to pass custom weights list for calculation
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])  #equal weights

#calculate the variance and risk of the portfolo
portfolio_variance = np.dot(weights.T, np.dot(cov_matrix_a, weights))
portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix_a, weights)))

percent_variance = str(round(portfolio_variance, 4) * 100) + '%'
percent_volatility = str(round(portfolio_volatility, 4) * 100) + '%'

print('The variance of your Portfolio is {}, and your Portfolio Risk is {}'
      .format(percent_variance, percent_volatility))
######Portfolio Standard Deviation END

######Sharpe Start

#set test variables
voo = "VOO"
btc = "Bitcoin"
portfolio_sharpe_ratio=1.5
voo_sharpe=1
btc_sharpe=2

#compare portfolio to voo and btc interchangeably
def higher_or_lower(portfolio, instrument):
    """Compare portfolio to VOO and BTC interchangeably"""
    #portfolio = portfolio_sharpe_ratio
    if portfolio > instrument:
        portfolio_vs_instrument = "higher"
    elif portfolio == instrument:
        portfolio_vs_instrument = "the same as"
    else:
        portfolio_vs_instrument = "lower"
    return portfolio_vs_instrument

f"""Your Sharpe Ratio is {portfolio_sharpe_ratio}.
 The risk adjusted retun of your portfolio is {higher_or_lower(portfolio_sharpe_ratio, voo_sharpe)} than that of {voo} ({voo_sharpe}) and 
 {higher_or_lower(portfolio_sharpe_ratio, btc_sharpe)} than that of {btc} ({btc_sharpe})"""
######Sharpe End

