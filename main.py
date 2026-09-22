from api_client import ApiClient
from data_manager import DataManager
from plotly_plotter import PlotlyPlotter
import plotly.graph_objects as go
import time


#User query for getting stock names
user_query = (input("Which stocks do you want to analyze? (separated by commas): ")).upper()
list_stocks = [stock.strip() for stock in user_query.split(",")]

fig = go.Figure()

data_manager = DataManager()
plotly_plot = PlotlyPlotter(fig)

#Flow to ask for individual plots
show_individual = False
if len(list_stocks) == 1:
    show_individual = True
else:
    individual_stock = input(
        "Besides the multi-stock comparison, do you want to see individual plots for these stocks? (Yes or No): ").lower().strip()
    if individual_stock == 'yes':
        show_individual = True

for stock in list_stocks:

### Download of data from API ###
    data_stock = ApiClient(stock)
    #Obtain stock data
    api_data = data_stock.data_request()
    # Check if too many queries used
    if api_data is None:
        print("Stopping process due to excess of API requests")
        break

### Creation of the dataframe ###
    #Create df
    stock_df = data_manager.dataframe_creation(api_data,stock)
    #Add variation column
    df_new_column = data_manager.addition_new_data(stock_df,stock)

### Plotting ###
    if show_individual:
        #Principal plot: Closing + MA
        plotly_plot.create_line_plot(df_new_column, [f'{stock} close value', f'{stock} moving average'], f'1. {stock} - Tendency and daily values')
        #Secondary plot: Daily change (Volatility)
        plotly_plot.create_line_plot(df_new_column, f'{stock} pct daily change', f'2. {stock} - Daily variation (volatility)')
    if len(list_stocks) > 1:
        # Principal plot: Base 100 for all stocks
        plotly_plot.create_multi_line_plot(df_new_column, f'{stock} base 100', stock)
    time.sleep(15)

if len(list_stocks) > 1:
    fig.update_layout(title_text="Performance Comparison (Base 100)")
    fig.show()


