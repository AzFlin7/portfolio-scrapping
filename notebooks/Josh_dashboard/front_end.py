#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import panel as pn
from panel.interact import interact
import dashboard 

import plotly.express as px
import panel as pn
get_ipython().run_line_magic('matplotlib', 'inline')
pn.extension("plotly")


# In[26]:


crypto_checkboxes = pn.widgets.CheckBoxGroup(name='Cryptocurrencies', value=['BTC'], 
                                  options=["BTC","XRP","ETH","LTC","BCH","XLM"],inline=True)

index_checkboxes = pn.widgets.CheckBoxGroup(name='Index', value=['VOO'], 
                                  options=["VOO","VXF","VEA","BSV","BNDX","FLRN"],inline=True)

crypto_row_upper = pn.Row(crypto_checkboxes)
crypto_row_lower = pn.Row(index_checkboxes)
select_button = pn.widgets.Button(name="Select these assets", button_type='primary')

def click_select_button_evnt(event):
    ticker_dict = {"crypto": crypto_checkboxes.value,
              "index": index_checkboxes.value}
    #print(ticker_dict)
    panel  = dashboard.get_dashboard(ticker_dict, mc_trials = 30)
    panel.show()
    #return ticker_dict
    
select_button.on_click(click_select_button_event)

crypto_rows_column = pn.Column(crypto_row_upper, crypto_row_lower, select_button)

crypto_rows_column.show()


# In[24]:




