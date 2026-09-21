from api_client import ApiClient
from data_manager import DataManager
from data_plotter import DataPlotter
import matplotlib.pyplot as plt
import time

#User query for getting stock names
user_query = (input("Which stocks do you want to analyze? (separated by commas): ")).upper()
list_stocks = [stock.strip() for stock in user_query.split(",")]

processed_stocks = 0

data_manager = DataManager()
data_plotter = DataPlotter()

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
    df_new_column = data_manager.daily_variation_addition(stock_df,stock)
    #Paint the stock line in plot
    plt.figure(1)
    data_plotter.add_line(df_new_column,f'{stock}_pct_daily_change', stock)
    plt.figure(2)
    data_plotter.add_line(df_new_column,'4. close', stock)
    # Avoid the API block due to too much requests
    time.sleep(15)
    processed_stocks += 1

if processed_stocks > 0:
    # Create plots
    plt.figure(1)
    data_plotter.save_plot("Daily variation")
    plt.figure(2)
    data_plotter.save_plot("Daily values")
else:
    print ("No data to plot")



