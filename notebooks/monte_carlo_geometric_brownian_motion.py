  
def mcs_brownian (df, num_simulations):
# Monte Carlo Simulation with Geometric Brownian Motion
# simulated_price = previous_day_price * exp((daily_returns_mean - ((daily_std_mean**2)/2)) + (daily_std_mean * random_noise ))
    
    daily_returns_df = df.pct_change()
    daily_returns_mean = daily_returns_df.mean()
    daily_std_mean = daily_returns_df.std()
    
    
    simulations = num_simulations
    trading_days = 252
    df_last_price = df[-1]

    
    simulated_price_df = pd.DataFrame()
    portfolio_cumulative_returns = pd.DataFrame()
    
    for n in range(simulations):
        
        simulated_prices = [df_last_price]
        
        for i in range (trading_days):
            drift = daily_returns_mean - (0.5*daily_std_mean**2)
            random_noise = np.random.normal()
            diffusion = (daily_std_mean * random_noise)
    
            simulated_price = simulated_prices[-1] * np.exp(drift + diffusion)
            simulated_prices.append(simulated_price)
            
        simulated_price_df = pd.Series(simulated_prices)
        simulated_daily_returns = simulated_price_df.pct_change()

        portfolio_cumulative_returns[n] = (1 + simulated_daily_returns.fillna(0)).cumprod()
    return portfolio_cumulative_returns
    