from api_client import ApiClient
from data_manager import DataManager
from matplotlib_plotter import MatplotlibPlotter
from plotly_plotter import PlotlyPlotter
import matplotlib.pyplot as plt
import time



#User query for getting stock names
# user_query = (input("Which stocks do you want to analyze? (separated by commas): ")).upper()
# list_stocks = [stock.strip() for stock in user_query.split(",")]

while True:
    user_query_plot = (input("Do you want Static or Live plots? ")).strip().lower()
    if user_query_plot == "live" or user_query_plot == "static":
        break

list_stocks = ['IBM']

processed_stocks = 0

data_manager = DataManager()
matplot_plot = MatplotlibPlotter()
plotly_plot = PlotlyPlotter()

for stock in list_stocks:
    data_stock = ApiClient(stock)
    #Obtain stock data
    api_data = data_stock.data_request()
    # Check if too many queries used
    if api_data is None:
        print("Stopping process due to excess of API requests")
        break
    #Create df
    stock_df = data_manager.dataframe_creation(api_data,stock)
    #Add variation column
    df_new_column = data_manager.addition_new_data(stock_df,stock)

    if user_query_plot == "static":
        #Paint the stock line in plot
        plt.figure(1)
        matplot_plot.add_line(df_new_column, f'{stock}_pct_daily_change', f'{stock} - Daily variation')
        plt.figure(2)
        matplot_plot.add_line(df_new_column, '4. close', f'{stock} - Daily values')
        matplot_plot.add_line(df_new_column, f'{stock}_moving_average', f'{stock} - Moving Average')
        # Avoid the API block due to too much requests
        time.sleep(15)
        processed_stocks += 1

        if processed_stocks > 0:
            # Create plots
            plt.figure(1)
            matplot_plot.save_plot("Daily variation")
            plt.figure(2)
            matplot_plot.save_plot("Daily values")
        else:
            print ("No data to plot")

    elif user_query_plot == "live":
        plotly_plot.create_plot_plotly(df_new_column,["4. close",f'{stock}_moving_average'])
        plotly_plot.create_plot_plotly(df_new_column, f'{stock}_pct_daily_change')


