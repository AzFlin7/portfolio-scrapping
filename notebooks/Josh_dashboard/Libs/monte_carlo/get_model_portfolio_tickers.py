def get_model_portfolio_tickers(model_portfolio):
# Will create a list of tickers for each model portfolio.  Accepts model portfolio name as a string 
# Model portfolios are fixed_income, conservative, moderately_conservative, balanced, moderately_aggressive, aggressive, all_equity
    
    model_portfolios = {'fixed_income' : {'BSV':0.267, 'BIV': 0.138, 'BLV': 0.129, 'VMBS': 0.152, 'BNDX': 0.294, 'FLRN': 0.02}}, {'conservative' : {'VOO': 0.098, 'VXF': 0.02, 'VEA': 0.06, 'VWO': 0.018, 'BSV': 0.213, 'BIV': 0.11, 'BLV': 0.104, 'VMBS': 0.122, 'BNDX': 0.235, 'FLRN': 0.02}}, {'moderately_conservative' : {'VOO': 0.195, 'VXF': 0.04, 'VEA': 0.121, 'VWO': 0.036, 'BSV': 0.16, 'BIV': 0.083, 'BLV': 0.083, 'VMBS': 0.091, 'BNDX': 0.176, 'FLRN': 0.02}}, {'balanced' : {'VOO': 0.244, 'VXF': 0.05, 'VEA': 0.151, 'VWO': 0.045, 'BSV': 0.133, 'BIV': 0.069, 'BLV': 0.065, 'VMBS': 0.076, 'BNDX': 0.147, 'FLRN': 0.02}}, {'moderately_aggressive' : {'VOO': 0.39, 'VXF': 0.08, 'VEA': 0.241, 'VWO': 0.073, 'BSV': 0.053, 'BIV': 0.028, 'BLV': 0.026, 'VMBS': 0.03, 'BNDX': 0.059, 'FLRN': 0.02}}, {'aggressive' : {'VOO': 0.39, 'VXF': 0.08, 'VEA': 0.241, 'VWO': 0.073, 'BSV': 0.053, 'BIV': 0.028, 'BLV': 0.026, 'VMBS': 0.03, 'BNDX': 0.059, 'FLRN': 0.02}}, {'all_equity' : {'VOO': 0.488, 'VXF': 0.10, 'VEA': .301, 'VWO': 0.091, 'FLRN': 0.02}}
    list_of_tickers = []
    
    for portfolios in model_portfolios:
        for portfolio, allocations in portfolios.items():
            if portfolio == model_portfolio:
                for ticker, weight in allocations.items():
                    list_of_tickers.append(ticker)
 
    return list_of_tickers