def click_select_button_evnt(event):
    ticker_dict = {"crypto": crypto_checkboxes.value,
              "index": index_checkboxes.value}
    #print(ticker_dict)
    panel  = dashboard.get_dashboard(ticker_dict, mc_trials = 30)
    panel.show()
    #return ticker_dict