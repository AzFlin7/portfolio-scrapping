#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pandas_datareader import data as web
#get_ipython().run_line_magic('matplotlib', 'inline')     <--- Christian is having an error with this, commented out to see if it breaks.
import hvplot.pandas
import libs.montecarlo as mc
import seaborn as sns
import panel as pn
import libs.apis as apis
from panel.interact import interact
import random
from path import Path
from iexfinance.stocks import get_historical_data
import iexfinance as iex


def get_assets_hist_data(tickers_dict={"index":[],"crypto":[]}, years=2):
    
    
    if ( len(tickers_dict["index"]) + len(tickers_dict["crypto"]) ) < 1:
              return "Empty list of assets"
        
    #Defining starting dat to get historical data.
    data_start_date = datetime.now() + timedelta(int(-365*years))

    #getting indeces historical prices form IEX
    if len(tickers_dict["index"]) > 0:
              print(f"received {tickers_dict['index']}")
              portfolio_indx_prices = apis.get_historic_data(ticker = tickers_dict["index"], 
                                                     start_date = data_start_date)
              if type(portfolio_indx_prices) == str:
                  print(portfolio_indx_prices)
                  return portfolio_indx_prices

    #getting cryptos historical prices form cryptocompare
    if len(tickers_dict["crypto"]) > 0:
              print(f"received {tickers_dict['crypto']}")
              btc_daily_price = apis.get_crypto_daily_price(tickers_dict["crypto"],limit=int(years*365))
              if type(btc_daily_price) == str:
                  print(btc_daily_price)
                  return btc_daily_price

    #Creating the portfolio dataframe depending on the kind of portfolio (crypto only, index only, or both)
    portfolio_hist_prices = pd.DataFrame()
    
    #For index only
    if len(tickers_dict["index"]) > 0 and len(tickers_dict["crypto"]) == 0:
              portfolio_hist_prices = portfolio_indx_prices
              print(portfolio_hist_prices.head())
        
    #For crypto only    
    elif len(tickers_dict["index"]) == 0 and len(tickers_dict["crypto"]) > 0:
              portfolio_hist_prices = btc_daily_price
              print(portfolio_hist_prices.head())
        
    #For both
    else: #concatenating both dataframes   
        portfolio_hist_prices = pd.concat([portfolio_indx_prices,btc_daily_price],axis=1,join="inner")
        print(portfolio_hist_prices.head())
        
          
    portfolio_hist_prices.dropna(inplace=True)
    portfolio_hist_prices = portfolio_hist_prices[(portfolio_hist_prices[portfolio_hist_prices.columns] != 0).all(axis=1)]

    #formating dataframes
    portfolio_hist_prices = apis.normalize_dataframe(portfolio_hist_prices)
    portfolio_daily_retn = portfolio_hist_prices.pct_change().copy()
    
    #Save both hist. prices and hist. daily returns dataframes packed in a list to be able to return in the funtion.
    hist_price_ret_df = [ portfolio_hist_prices, portfolio_daily_retn ]
    
    return hist_price_ret_df


def corr_plot(portfolio_daily_retn):
    title_font = {'family': 'monospace',
            'color':  'blue',
            'weight': 'bold',
            'size': 15,
            }
    correlated = portfolio_daily_retn.corr()
    # Generate a mask for the upper triangle
    mask = np.zeros_like(correlated, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    correlated_plot, ax = plt.subplots(figsize=(12, 8))

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(correlated, mask=mask, cmap="coolwarm", vmax=1, vmin =-1, 
                center=0,square=True, linewidths=.5, annot=True )
    plt.title(f"Correlation Map of Portfolio\n",fontdict=title_font)
    #ax.set_facecolor("aliceblue")

     #correlated_plot = sns.heatmap(correlated, vmin=-1, vmax=1, annot=True,cmap="coolwarm") 
    plt.close()
    return pn.Pane(correlated_plot)

def get_corr_pane(portfolio_daily_retn):
    marqu_txt = apis.get_marquee_text()   
   
    m_text = pn.panel( 
    marqu_txt, 
    align = "center"
    )

    side_text = pn.pane.Markdown(
'''
<style>

body {
    background-color: #FFFFFF;
}

mar {
  color: #000000;
  text-align: center;
  font-family: "Times New Roman", Times, serif;
  font-style: normal;
  font-size: 17px;
}

#leftbox {
    color: black;
}

bold{
    font-weight: bold;
    color: #993300;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-style: oblique;
    font-size: 24px;
    font-variant: small-caps;
}
p {
  color: #000000;
}

p1 {
  color: #006600;
  font-size: 17px;
}

h1 {
    font-size: 30px;
    font-variant: small-caps;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

h2 {
  color: #000000;
  font-family: Arial, Helvetica, sans-serif;
}

h3 {
    color: #000000
    font-size: 16px;
    font-style: italic;
}

cr {
    font-size: 14px;
    font-style: italic;
    color: #33CCFF;
}
</style>
            
<div id="leftbox"> 
<h1>The Correlation Heat Map</h1>
</div>
---
<h2> What is Correlation?</h2>

<p1> Correlation between sets of data is a measure of how well they are related. The most common measure of correlation in stats is the Pearson Correlation. 
The full name is the Pearson Product Moment Correlation (PPMC). It shows the linear relationship between two sets of data. In simple terms, it answers the question, Can I draw a line graph to represent the data? </p1>
<cr><a href='https://www.statisticshowto.datasciencecentral.com/probability-and-statistics/correlation-coefficient-formula/#Pearson', 
target="_blank"> Statistics How To</a></cr> 
<br><p>Learn more at <a href='https://www.statisticshowto.datasciencecentral.com/probability-and-statistics/correlation-coefficient-formula/#Pearson', target="_blank">https://www.statisticshowto.datasciencecentral.com/probability-and-statistics/correlation-coefficient-formula/#Pearson</a>
''',
        align= "center",
        width_policy = "max",
    )
    
    lower_text = pn.pane.Markdown('''
<h3><bold>Important:</bold> &nbsp;Correlation does not imply causation!</h3>
---
        ''',
                                  align= "center",
                                  width_policy = "max",
                                  margin=(0, 50),
                                 )###??????????
    #WARNING:param.Markdown11741: Setting non-parameter attribute
    #max_with=5 using a mechanism intended only for parameters
    left_row = pn.Row(side_text, align="start")
    middle_row = pn.Row(corr_plot(portfolio_daily_retn),align="center", width_policy="fit")
    both_row = pn.Row(left_row, middle_row)
    
    corr_pane = pn.Column(m_text,both_row,lower_text,align="center", sizing_mode='stretch_both')
    
    return corr_pane
    
    

def sharp_rt_plot(portfolio_daily_retn):
    
    title_font = {'family': 'monospace',
            'color':  'blue',
            'weight': 'bold',
            'size': 15,
            }
    label_font = {'family': 'monospace',
            'color':  'green',
            'weight': 'bold',
            'size': 12,
            }
   
    bar_colors=["midnightblue","royalblue","indigo","darkcyan","darkgreen","maroon",
               "purple","darkorange","slategray","forestgreen", "darkgoldenrod", "sienna"]

    sharp_ratios = portfolio_daily_retn.mean()*np.sqrt(252)/portfolio_daily_retn.std()

    sr_plot = plt.figure(figsize = (12,8));
    plt.bar(x = sharp_ratios.index, height=sharp_ratios,  color=random.sample(bar_colors,len(sharp_ratios.index)))
    plt.title(f"Sharpe Ratios of Portfolio\n",fontdict=title_font)
    plt.ylabel("Sharpe Ratio",fontdict=label_font)
    plt.xlabel("Assets",fontdict=label_font)
    plt.axhline(sharp_ratios.mean(), color='r')
    plt.close()
    return pn.Pane(sr_plot)



def get_sharp_pane(portfolio_daily_retn):
    marqu_txt = apis.get_marquee_text()   
   
    m_text = pn.panel( 
    marqu_txt, 
    align = "center"
    )

    side_text = pn.pane.Markdown(
'''
<style>

body {
    background-color: #FFFFFF;
}

mar {
  color: #000000;
  text-align: center;
  font-family: "Times New Roman", Times, serif;
  font-style: normal;
  font-size: 17px;
}

#leftbox {
    color: black;
}

bold{
    font-weight: bold;
    color: #993300;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-style: oblique;
    font-size: 24px;
    font-variant: small-caps;
}
p {
  color: #000000;
}

p1 {
  color: #006600;
  font-size: 17px;
}

h1 {
    font-size: 30px;
    font-variant: small-caps;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

h2 {
  color: #000000;
  font-family: Arial, Helvetica, sans-serif;
}

h3 {
    color: #000000
    font-size: 15px;
    font-style: italic;
}

cr {
    font-size: 14px;
    font-style: italic;
    color: #33CCFF;
}
</style>
            
<div id="leftbox"> 
<h1>The Sharpe Ratio</h1>
</div>
---
<h2> What is the Sharpe Ratio?</h2>

<p1> The Sharpe ratio was developed by Nobel laureate William F. Sharpe and is used to help investors understand the return of an investment compared to its risk. The ratio is the average return earned in excess of the risk-free rate per unit of volatility or total risk.
Subtracting the risk-free rate from the mean return allows an investor to better isolate the profits associated with risk-taking activities. Generally, the greater the value of the Sharpe ratio, the more attractive the risk-adjusted return.</p1>
<cr><a href='https://www.investopedia.com/terms/s/sharperatio.asp', 
target="_blank"> - Investopedia</a></cr> 
<br><p>Learn more at <a href='https://www.investopedia.com/terms/s/sharperatio.asp', target="_blank">https://www.investopedia.com/terms/s/sharperatio.asp</a>
''',
        align= "center",
        width_policy = "max",
    )
    
    lower_text = pn.pane.Markdown('''
<h3>The Sharpe ratio is calculated by subtracting the risk-free rate from the return of the portfolio and dividing that result by the standard deviation of the portfolio’s excess return.</h3>
---
        ''',
                                  align= "center",
                                  width_policy = "max",
                                  margin=(0, 50),
                                 )###??????????
    #WARNING:param.Markdown11741: Setting non-parameter attribute
    #max_with=5 using a mechanism intended only for parameters
    left_row = pn.Row(side_text, align="start")
    middle_row = pn.Row(sharp_rt_plot(portfolio_daily_retn),align="center", width_policy="fit")
    both_row = pn.Row(left_row, middle_row)
    
    sharpe_pane = pn.Column(m_text,both_row,lower_text,align="center", sizing_mode='stretch_both')
    
    return sharpe_pane




def plot_mont_carl(monte_carlo_sim):
    plot_title = f"Monte Carlo Simulation of Portfolio"
    monte_carlo_sim_plot = monte_carlo_sim.hvplot(title=plot_title,figsize=(35,20),legend=False)
    return monte_carlo_sim_plot


def get_monte_pane(portfolio_daily_retn):
    marqu_txt = apis.get_marquee_text()   
   
    m_text = pn.panel( 
    marqu_txt, 
    align = "center"
    )

    side_text = pn.pane.Markdown(
'''
<style>

body {
    background-color: #FFFFFF;
}

mar {
  color: #000000;
  text-align: center;
  font-family: "Times New Roman", Times, serif;
  font-style: normal;
  font-size: 17px;
}

#leftbox {
    color: black;
}

bold{
    font-weight: bold;
    color: #993300;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-style: oblique;
    font-size: 24px;
    font-variant: small-caps;
}
p {
  color: #000000;
}

p1 {
  color: #006600;
  font-size: 17px;
}

h1 {
    font-size: 30px;
    font-variant: small-caps;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

h2 {
  color: #000000;
  font-family: Arial, Helvetica, sans-serif;
}

h3 {
    color: #000000
    font-size: 15px;
    font-style: italic;
}

cr {
    font-size: 14px;
    font-style: italic;
    color: #33CCFF;
}
</style>
            
<div id="leftbox"> 
<h1>The Monte Carlo Simulation</h1>
</div>
---
<h2> What is a Monte Carlo Simulation?</h2>

<p1>Monte Carlo simulations are used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is a technique used to understand the impact of risk and uncertainty in prediction and forecasting models.
<br>
Monte Carlo simulation can be used to tackle a range of problems in virtually every field such as finance, engineering, supply chain, and science.
<br>
Monte Carlo simulation is also referred to as multiple probability simulation.
</p1>
<cr><a href='https://www.investopedia.com/terms/m/montecarlosimulation.asp', 
target="_blank"> - Investopedia</a></cr> 
<br><p>Learn more at <a href='https://www.investopedia.com/terms/m/montecarlosimulation.asp', target="_blank">https://www.investopedia.com/terms/m/montecarlosimulation.asp</a>
''',
        align= "center",
        width_policy = "max",
    )
    
    lower_text = pn.pane.Markdown('''
<h3>When faced with significant uncertainty in the process of making a forecast or estimation, rather than just replacing the uncertain variable with a single average number, the Monte Carlo Simulation might prove to be a better solution.</h3>
---
        ''',
                                  align= "center",
                                  width_policy = "max",
                                  margin=(0, 50),
                                 )###??????????
    #WARNING:param.Markdown11741: Setting non-parameter attribute
    #max_with=5 using a mechanism intended only for parameters
    left_row = pn.Row(side_text, align="start")
    middle_row = pn.Row(plot_mont_carl(portfolio_daily_retn),align="center", width_policy="fit")
    both_row = pn.Row(left_row, middle_row)
    
    monte_pane = pn.Column(m_text,both_row,lower_text,align="center", sizing_mode='stretch_both')
    
    return monte_pane


def get_conf_interval(last_row_db,q=[0.05, 0.95]):
    confidence_interval = last_row_db.quantile(q=q)
    return confidence_interval


def plot_conf(values=None,conf=[0,0]):
    conifidence_plot = plt.figure(figsize=(12,8));
    plt.hist(x = values,bins=20)
    plt.axvline(conf.iloc[0], color='r')
    plt.axvline(conf.iloc[1], color='r')
    plt.close()
    return pn.Pane(conifidence_plot)

def get_conf_pane(mc_sim):
    marqu_txt = apis.get_marquee_text()   
   
    m_text = pn.panel( 
    marqu_txt, 
    align = "center"
    )

    side_text = pn.pane.Markdown(
'''
<style>

body {
    background-color: #FFFFFF;
}

mar {
  color: #000000;
  text-align: center;
  font-family: "Times New Roman", Times, serif;
  font-style: normal;
  font-size: 17px;
}

#leftbox {
    color: black;
}

bold{
    font-weight: bold;
    color: #993300;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-style: oblique;
    font-size: 24px;
    font-variant: small-caps;
}
p {
  color: #000000;
}

p1 {
  color: #006600;
  font-size: 17px;
}

h1 {
    font-size: 30px;
    font-variant: small-caps;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

h2 {
  color: #000000;
  font-family: Arial, Helvetica, sans-serif;
}

h3 {
    color: #000000
    font-size: 15px;
    font-style: italic;
}

cr {
    font-size: 14px;
    font-style: italic;
    color: #33CCFF;
}
</style>
            
<div id="leftbox"> 
<h1>The Monte Carlo Simulation Confidence Intervals</h1>
</div>
---
<h2> What are Confidence Intervals?</h2>

<p1>A confidence interval is an interval that will contain a population parameter a specified proportion of the time. The confidence interval can take any number of probabilities, with the most common being 95% or 99%.
<br>
Statisticians use confidence intervals to measure uncertainty. A higher probability associated with the confidence interval means that there is a greater degree of certainty that the parameter falls within the bounds of the interval. 
</p1>
<cr><a href='https://www.investopedia.com/terms/c/confidenceinterval.asp', 
target="_blank"> - Investopedia</a></cr> 
<br><p>Learn more at <a href='https://www.investopedia.com/terms/c/confidenceinterval.asp', target="_blank">https://www.investopedia.com/terms/c/confidenceinterval.asp</a>
 
''',
        align= "center",
        width_policy = "max",
    )
    
    lower_text = pn.pane.Markdown('''
<h3>The biggest misconception regarding confidence intervals is that they represent the percentage of data from a given sample that falls between the upper and lower bounds.</h3>
---
        ''',
                                  align= "center",
                                  width_policy = "max",
                                  margin=(0, 50),
                                 )###??????????
    #WARNING:param.Markdown11741: Setting non-parameter attribute
    #max_with=5 using a mechanism intended only for parameters
    left_row = pn.Row(side_text, align="start")
    middle_row = pn.Row(plot_conf(mc_sim.iloc[-1],get_conf_interval(mc_sim.iloc[-1])),align="center", width_policy="fit")
    both_row = pn.Row(left_row, middle_row)
    
    conf_pane = pn.Column(m_text,both_row,lower_text,align="center", sizing_mode='stretch_both')
    
    return conf_pane

# New panel code for report

def get_report_pane(mc_sim, overall_sharpe):
    marqu_txt = apis.get_marquee_text()   
   
    m_text = pn.panel( 
    marqu_txt, 
    align = "center"
    )

    side_text = pn.pane.Markdown(
'''
<style>

body {
    background-color: #FFFFFF;
}

mar {
  color: #000000;
  text-align: center;
  font-family: "Times New Roman", Times, serif;
  font-style: normal;
  font-size: 17px;
}

#leftbox {
    color: black;
}

bold{
    font-weight: bold;
    color: #993300;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-style: oblique;
    font-size: 24px;
    font-variant: small-caps;
}
p {
  color: #000000;
}

p1 {
  color: #006600;
  font-size: 17px;
}

h1 {
    font-size: 30px;
    font-variant: small-caps;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

h2 {
  color: #000000;
  font-family: Arial, Helvetica, sans-serif;
}

h3 {
    color: #000000
    font-size: 15px;
    font-style: italic;
}

cr {
    font-size: 14px;
    font-style: italic;
    color: #33CCFF;
}
</style>
            
<div id="leftbox"> 
<h1>The Analysis Report</h1>
</div>''' f'''
---
<h2> Should I Add Crypto Currencies to My Portfolio?</h2>
</br>
<p1>Using a static investment of ${initial_investment}.00 USD we have predicted the potential earnings of your porfolio in comparison to the some of the most common standard portfolios.  Due to the age and volitilty of crypto curriences we have restricted our simulations to a one year period.
</br>
---

Based on 100 simulations here is the 95% confidence interval range of your portfolio earnings compared to traditional portfolios:</br>

Your Portfolio: ${get_conf_interval_lower(mc_sim.iloc[-1])} to ${get_conf_interval_higher(mc_sim.iloc[-1])}</br>
Aggressive Portfolio: ${times_initial(aggressive_low)} to ${times_initial(aggressive_high)}</br>
Balanced Portfolio: ${times_initial(balanced_low)} to ${times_initial(balanced_high)}</br>
Conservative Portfolio: ${times_initial(conservative_low)} to ${times_initial(conservative_high)}</br>
</br>
---
One of the best ways to compare and assess risk is through the Sharpe Ratio. The Sharpe Ratio of your selected portfolio is {overall_sharpe},
its risk adjusted return is {more_or_less_by(overall_sharpe, aggressive_sharpe_t)} {higher_or_lower(overall_sharpe, aggressive_sharpe_t)} compared to the Aggressive portfolio, {more_or_less_by(overall_sharpe, balanced_sharpe_t)} {higher_or_lower(overall_sharpe, balanced_sharpe_t)} than the Balanced portfolio, and {more_or_less_by(overall_sharpe, conservative_sharpe_t)} {higher_or_lower(overall_sharpe, conservative_sharpe_t)} than the Conservative portfolio. </br></p1>

 
''',
        align= "center",
        #width_policy = "max",
        width = 500
    )
    
    lower_text = pn.pane.Markdown(f'''
<h3>Thanks for using the Melting Pot of Freedom!</h3>
---
        ''',
                                  align= "center",
                                  width_policy = "max",
                                  margin=(0, 50),
                                 )###??????????
    #WARNING:param.Markdown11741: Setting non-parameter attribute
    #max_with=5 using a mechanism intended only for parameters
    left_row = pn.Row(side_text, align="start")
    middle_row = pn.Row(sharpe_comparision_plot(conservative_sharpe_t,balanced_sharpe_t,aggressive_sharpe_t,overall_sharpe),align="center", width_policy="fit", margin = (40,40)) #Add any plots of images here to this row.  if you need them to stack then make a column and and add the column in place of the current monte plot
    both_row = pn.Row(left_row, middle_row)
    
    report_pane = pn.Column(m_text,both_row,lower_text,align="center", sizing_mode='stretch_both')
    
    return report_pane

###functions begin

    
def more_or_less_by(portfolio, portfolio_comparison):
    """Input user portfolio and comparison to get difference"""
    if portfolio > portfolio_comparison:
        difference = round((portfolio - portfolio_comparison), 2)
    elif portfolio < portfolio_comparison:
        difference = round((portfolio_comparison - portfolio), 2)
    else:
        difference = 0
    return difference

def higher_or_lower(portfolio, portfolio_comparison):
    """input user portfolio and pre-selected to get higher or lower answer"""
    if portfolio > portfolio_comparison:
        portfolio_vs_comparison = "higher"
    elif portfolio == portfolio_comparison:
        portfolio_vs_comparison = "the same as"
    else:
        portfolio_vs_comparison = "lower"
    return portfolio_vs_comparison

def port_percent_variance(daily_returns):
    """Calculate portfolio variance with daily returns"""
    cov_matrix_d = daily_returns.cov()
    cov_matrix_a = cov_matrix_d * 252

    weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    #calculate portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix_a, weights))

    percent_variance = (round(portfolio_variance, 4) * 100)
    return percent_variance

def port_percent_volatility(daily_returns):
    """Calculate portfolio volatility with daily returns"""
    cov_matrix_d = daily_returns.cov()
    cov_matrix_a = cov_matrix_d * 252

    weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    #calculate portfolo risk
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix_a, weights)))
    
    percent_volatility = (round(portfolio_volatility, 4) * 100)
    return percent_volatility

def times_initial(portfolio_confidence):
    """Multiply model portfolio confidence interval by initial investment"""
    performance = portfolio_confidence * initial_investment
    return int(performance)

def get_conf_interval_higher(last_row_db,q=[0.05, 0.95]):
    """Get higher user portfolio confidence interval multiplied by initial investment"""
    confidence_interval = last_row_db.quantile(q=q)
    higher_confidence = confidence_interval[0.95]
    output = higher_confidence * initial_investment
    return int(output)

def get_conf_interval_lower(last_row_db,q=[0.05, 0.95]):
    """Get lower user portfolio confidence interval multiplied by initial investment"""
    confidence_interval = last_row_db.quantile(q=q)
    lower_confidence = confidence_interval[0.05]
    output = lower_confidence * initial_investment
    return int(output)


import pandas as pd 
import numpy as np
from path import Path

def get_conservative_confidence_intervals():
# This function will return a tuple that has the lower bound as the first value 
# and the upper boundary is the 2nd value, multiply both of these by the initial investment to get
# the simulated range of the ending value of your investment
    
    file_path= Path("model_data/Conservative_portfolio/Resources/conservative_simulated_cumulative_returns.csv")
    conservative_simulated_returns = pd.read_csv(file_path)
    conservative_simulated_ending_returns = conservative_simulated_returns.iloc[-1,:]
    conservative_confidence_interval = conservative_simulated_ending_returns.quantile(q=[0.05,0.95])
    conservative_confidence_interval_lowerbound = conservative_confidence_interval.iloc[0]
    conservative_confidence_interval_upperbound = conservative_confidence_interval.iloc[1]
    return conservative_confidence_interval_lowerbound, conservative_confidence_interval_upperbound

def get_balanced_confidence_intervals():
# This function will return a tuple that has the lower bound as the first value 
# and the upper boundary is the 2nd value, multiply both of these by the initial investment to get
# the simulated range of the ending value of your investment
    
    file_path = Path("model_data/Balanced_portfolio/Resources/balanced_cumulative_returns.csv")
    balanced_simulated_returns = pd.read_csv(file_path)
    balanced_simulated_ending_returns = balanced_simulated_returns.iloc[-1,:]
    balanced_confidence_interval = balanced_simulated_ending_returns.quantile(q=[0.05,0.95])
    balanced_confidence_interval_lowerbound = balanced_confidence_interval.iloc[0]
    balanced_confidence_interval_upperbound = balanced_confidence_interval.iloc[1]
    return balanced_confidence_interval_lowerbound, balanced_confidence_interval_upperbound

def get_aggressive_confidence_intervals():
# This function will return a tuple that has the lower bound as the first value 
# and the upper boundary is the 2nd value, multiply both of these by the initial investment to get
# the simulated range of the ending value of your investment
    
    file_path = Path("model_data/Aggressive_portfolio/Resources/aggressive_cumulative_returns.csv")
    aggressive_simulated_returns = pd.read_csv(file_path)
    aggressive_simulated_ending_returns = aggressive_simulated_returns.iloc[-1,:]
    aggressive_confidence_interval = aggressive_simulated_ending_returns.quantile(q=[0.05,0.95])
    aggressive_confidence_interval_lowerbound = aggressive_confidence_interval.iloc[0]
    aggressive_confidence_interval_upperbound = aggressive_confidence_interval.iloc[1]
    return aggressive_confidence_interval_lowerbound, aggressive_confidence_interval_upperbound



def get_model_portfolio_sharpe_ratios():
# This function will return the sharpe ratios for the conservative, balanced, and aggressive portfolios. It will return a tuple with the values being in order conservative, balanced, aggressive
    conservative_filepath = Path("model_data/Conservative_portfolio/Resources/conservative_hist_daily_returns.csv")
    balanced_filepath = Path("model_data/Balanced_portfolio/Resources/balanced_hist_daily_returns.csv")
    aggressive_filepath = Path("model_data/Aggressive_portfolio/Resources/aggressive_hist_daily_returns.csv")
    
    conservative_hist_returns = pd.read_csv(conservative_filepath)
    balanced_hist_returns = pd.read_csv(balanced_filepath)
    aggressive_hist_returns = pd.read_csv(aggressive_filepath)
    
    conservative_sharpe_ratios = conservative_hist_returns.mean()*np.sqrt(252)/conservative_hist_returns.std()
    balanced_sharpe_ratios = balanced_hist_returns.mean()*np.sqrt(252)/balanced_hist_returns.std()
    aggressive_sharpe_ratios = aggressive_hist_returns.mean()*np.sqrt(252)/aggressive_hist_returns.std()
    
    conservative_sharpe_ratios_db = pd.DataFrame(conservative_sharpe_ratios)
    conservative_sharpe_ratios_db.rename(columns = {0:'std'}, inplace = True)
    balanced_sharpe_ratios_db = pd.DataFrame(balanced_sharpe_ratios)
    balanced_sharpe_ratios_db.rename(columns = {0:'std'}, inplace = True)
    aggressive_sharpe_ratios_db = pd.DataFrame(aggressive_sharpe_ratios)
    aggressive_sharpe_ratios_db.rename(columns = {0:'std'}, inplace = True)
    
    conservative_weights = [0.098,0.02,0.06,0.018,0.213,0.11,0.104,0.122,0.235,0.02]
    conservative_overall_sharpe_ratio = conservative_sharpe_ratios_db.multiply(conservative_weights, axis = 0)
    balanced_weights = [0.244, .05, 0.151,0.045,0.133,0.069,0.065,0.076,0.147,0.02]
    balanced_overall_sharpe_ratio = balanced_sharpe_ratios_db.multiply(balanced_weights, axis = 0)
    aggressive_weights = [0.39,0.08,0.241,0.073,0.053,0.028,0.026,0.03,0.059,0.02]
    aggressive_overall_sharpe_ratio = aggressive_sharpe_ratios_db.multiply(aggressive_weights, axis = 0)
    
    conservative_overall_sharpe_ratio = conservative_overall_sharpe_ratio.sum()
    balanced_overall_sharpe_ratio = balanced_overall_sharpe_ratio.sum()
    aggressive_overall_sharpe_ratio = aggressive_overall_sharpe_ratio.sum()
    
    conservative_overall_sharpe_ratio = round(conservative_overall_sharpe_ratio[0], 2)
    balanced_overall_sharpe_ratio = round(balanced_overall_sharpe_ratio[0], 2)
    aggressive_overall_sharpe_ratio = round(aggressive_overall_sharpe_ratio[0], 2)
    
    return conservative_overall_sharpe_ratio,balanced_overall_sharpe_ratio,aggressive_overall_sharpe_ratio

### combined Sharpe Plot
def sharpe_comparision_plot(conservative_sharpe_t,balanced_sharpe_t,aggressive_sharpe_t,overall_sharpe):
    sharpe_series = pd.Series([conservative_sharpe_t,balanced_sharpe_t,aggressive_sharpe_t,overall_sharpe])
    sharpe_db = pd.DataFrame(sharpe_series)
    sharpe_db.rename(index = {0: 'conservative', 1: 'balanced', 2: 'aggressive', 3:'custom'}, inplace = True)
    sharpe_comparision_plot = sharpe_db.hvplot.bar(value_label="Sharpe Ratio",ylabel="Sharpe Ratio")
    return sharpe_comparision_plot

    


###functions end

#variables to keep
initial_investment=30000
aggressive = get_aggressive_confidence_intervals()
aggressive_conf = aggressive[-1]*initial_investment
balanced = get_balanced_confidence_intervals()
balanced_conf = balanced[-1]*initial_investment
conservative = get_conservative_confidence_intervals()
conservative_conf = conservative[-1]*initial_investment

aggressive_low, aggressive_high = get_aggressive_confidence_intervals()
balanced_low, balanced_high = get_balanced_confidence_intervals()
conservative_low , conservative_high = get_conservative_confidence_intervals()
conservative_sharpe_t, balanced_sharpe_t, aggressive_sharpe_t = get_model_portfolio_sharpe_ratios()
sharpe_ratios = []
sharpe_ratios = get_model_portfolio_sharpe_ratios

#calling global df
#sharpe_ratios = portfolio_daily_global.mean()*np.sqrt(252)/portfolio_daily_global.std()


# End

def get_dashboard(tickers_dict={"index":[],"crypto":[]}, years=2, mc_trials=500, mc_sim_days=252, weights=None):
    #clean this mess later:
    #weights = None must cease to exist
    #find a better way to do this... etc.
    print(tickers_dict)
    print(tickers_dict["index"]["weights"])
    tickers_only = {"index":tickers_dict["index"]["ticker"],"crypto":tickers_dict["crypto"]["ticker"]}
                    
    data = get_assets_hist_data(tickers_dict=tickers_only, years=years)
    if type(data) == str:
        return data
    
                    
    weights = tickers_dict["index"]["weights"] + tickers_dict["crypto"]["weights"]
    print(weights)
    
    
                    
    mc_sim = mc.monte_carlo_sim(data[0],trials = mc_trials, sim_days = mc_sim_days, weights = weights)
    #reset variables to clean old data remanents
    #years, mc_trials, mc_sim_days, weights = 2,500, 252, None
    #if type(mc_sim) == str: print(mc_sim)

    
    ### user portfolio sharpe ratio
    
    sharpe_ratios_local = data[1].mean()*np.sqrt(252)/data[1].std()
    overall_sharpe = round(sharpe_ratios_local.multiply(weights, axis=0).sum(), 2)
    
    ##
    
    risk_tabs = pn.Tabs(
        ("Correlation of portfolio",get_corr_pane(data[1])),
        
        #background="whitesmoke"
    )

    sharpe_tab = pn.Tabs(
        ("Sharp Ratios", get_sharp_pane(data[1])),
    )
    ###
    montecarlo_tabs = pn.Tabs(
        ("Monte Carlo Simulation",get_monte_pane(mc_sim)),
        ("Confidence Intervals", get_conf_pane(mc_sim)),
        #background="whitesmoke"
    )

    tabs = pn.Tabs(
        ("Correlation",risk_tabs),
        ("Sharpe Ratio", sharpe_tab),
        ("Monte Carlo Simulation", montecarlo_tabs),
        ("Report", get_report_pane(mc_sim, overall_sharpe)),
        #background="whitesmoke",
        tabs_location = "left",
        align = "start"
    )

    panel = tabs
    
    years, mc_trials, mc_sim_days, weights = 2,500, 252, None
    if type(mc_sim) == str: print(mc_sim)
    
    return panel


# In[ ]:




