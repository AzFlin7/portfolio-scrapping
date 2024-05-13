#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import hvplot.pandas
import montecarlo as mc
import seaborn as sns
import panel as pn
from panel.interact import interact
import random

from iexfinance.stocks import get_historical_data
import iexfinance as iex


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
               "purple","darkorange","slategray","forestgreen"]

    sharp_ratios = portfolio_daily_retn.mean()*np.sqrt(252)/portfolio_daily_retn.std()

    sr_plot = plt.figure(figsize = (12,8));
    plt.bar(x = sharp_ratios.index, height=sharp_ratios,  color=random.sample(bar_colors,len(sharp_ratios.index)))
    plt.title(f"Sharp Ratios of Portfolio\n",fontdict=title_font)
    plt.ylabel("Sharp Ratio",fontdict=label_font)
    plt.xlabel("Assets",fontdict=label_font)
    plt.axhline(sharp_ratios.mean(), color='r')
    plt.close()
    return pn.Pane(sr_plot)


#monte_carlo_sim = mc.monte_carlo_sim(df=portfolio_hist_prices, trials=10, sim_days=252)

def plot_mont_carl(monte_carlo_sim):
    plot_title = f"Monte-Carlo Simulation of Portfolio"
    monte_carlo_sim_plot = monte_carlo_sim.hvplot(title=plot_title,figsize=(27,15),legend=False)
    return monte_carlo_sim_plot


def get_conf_interval(last_row_db,q=[0.05, 0.95]):
    confidence_interval = last_row_db.quantile(q=q)
    return confidence_interval


def plot_conf(values=None,conf=[0,0]):
    confidence_plot = plt.figure(figsize=(12,8));
    plt.hist(x = values,bins=20)
    plt.axvline(conf.iloc[0], color='r')
    plt.axvline(conf.iloc[1], color='r')
    plt.close()
    return pn.Pane(confidence_plot)


def get_dashboard(tickers_dict={"index":[],"crypto":[]}, years=2, mc_trials=500, mc_sim_days=252, weights=None):
    
    data = get_assets_hist_data(tickers_dict=tickers_dict, years=years)
    
    mc_sim = mc.monte_carlo_sim(data[0],trials = mc_trials, sim_days = mc_sim_days, weights = weights)
    #reset variables to clean old data remanents
    years, mc_trials, mc_sim_days, weights = 2,500, 252, None
    if type(mc_sim) == str: print(mc_sim)
    
    risk_tabs = pn.Tabs(
        ("Correlation of portfolio",corr_plot(data[1])),
        ("Sharp Ratios", sharp_rt_plot(data[1])),
        #background="whitesmoke"
    )


    montecarlo_tabs = pn.Tabs(
        ("monte Carlo Simulation",plot_mont_carl(mc_sim)),
        ("Confidence Intervals", plot_conf(mc_sim.iloc[-1],get_conf_interval(mc_sim.iloc[-1]))),
        #background="whitesmoke"
    )

    techl_analysis_tabs = pn.Tabs(
        ("TA1","in construction"),
        ("TA2", "in construction"),
        #background="whitesmoke"
    )

    tabs = pn.Tabs(
        ("Risk",risk_tabs),
        ("Monte Carlo Simulation", montecarlo_tabs),
        ("Tecnical Analysis", techl_analysis_tabs),
        ("Report", "in construction"),
        #background="whitesmoke",
        tabs_location = "left",
        align = "start"
    )

    panel = tabs

    return panel


# In[ ]:




