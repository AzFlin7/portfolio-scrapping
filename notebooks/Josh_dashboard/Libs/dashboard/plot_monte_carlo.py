def plot_monte_carlo(monte_carlo_sim):
    plot_title = f"Monte-Carlo Simulation of Portfolio"
    monte_carlo_sim_plot = monte_carlo_sim.hvplot(title=plot_title,figsize=(27,15),legend=False)
    return monte_carlo_sim_plot