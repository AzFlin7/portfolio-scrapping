# Crypto Portfolio analysis

### Create custom portfolios with crypto currencies and compare them to traditional portfolios
<br>

_Generate a custom portfolio, and pull real time data via Crypto Compare API and IEX Finance API.  The data is then cleaned and a Sharpe Ratio, Heatmap, Monte Carlo, and confidence interval functions are then run on the data.  The resulting plots are then served up to a panel via a local Bokeh Server._

<br>

**Dependencies:** <br>
    Plotly Express: ` pip install plotly-express `<br>
    Numpy: ` pip install numpy `<br>
    Pandas:`pip install pandas`<br>
    PyViz: `pip install pyviz`<br>
    Plotly:`pip install plotly`<br>
    Seaborn: `pip install seaborn`<br>
    TA for Python : `pip install ta`<br>
    iexfinance: `pip install iexfinance`<br>
 
<br>

**API Keys:**<br>
   IEX Finance declared in environmental variables as : `IEX_TOKEN: pk_......`<br>
   [Get Your Free Keys Here](https://www.iexcloud.io/)
   
   Crypto Compare declared in environmental variables as : `CC_API: ........`<br>
   [Get Your Free Keys Here](https://min-api.cryptocompare.com/)
   <br>

   ## Description

   _This project has been developed using only python and HTML although some libraries make use of JavaScrip in the background._

   The initial page is built of three main sections. The first one will show you the last 45 days of the price of different cryptocurrencies and will also display some Technical Analysis (TA) indicators on top of the price curve. The second one is a basic explanaition of the project, and the third one is where the user will select the portfolio components with their respective preponderance weights.
  
  ![Initial page][initialWindow]

   [initialWindow]: images/initial_page.png

   To create your custom portfolio simply select the tickers and add the weight in the portfolio for each one at the bottom of the page. Remember that the total sum of the weights must equal 1.0.

![User input][settingValues]

   [settingValues]: images/settingValues.png

Once you have selected the stock indices and cryptocurrencies that will be part of your portfolio, you can see the fully report of risk/profit analysis.

This section will have four different tabs, the first one being the correlation chart which will show how diversified your portfolio is.

![Initial page][correlation]

   [correlation]: images/correlation.png

The other tabs will show the sharp ratios which will show how much profit over unit of risk each index or cryptocurrency has added individually to your portfolio.

![Sharp Ratios][sharp_ratios]

[sharp_ratios]: images/sharp_ratios.png

The Montecarlo simulation is displayed in the next tab. This simulation is a totally randomic simulation which will show the most likely values that your portfolio is going to take over the course of a year. This sections is built from 2 tabs.

![Montecarlo][montecarlo]

[montecarlo]: images/montecarlo.png

![Confidence Intervals][confidence_intervals]

[confidence_intervals]: images/confidence_values.png
   
Finally, we get the fully report generated based on the results of the different analysis. This report will compare your custome portfolio with some standard portfolios managed by most banks in the US.

![Final Report][report]

[report]: images/report.png