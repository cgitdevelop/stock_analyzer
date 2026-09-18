import pandas as pd
from api_client import ApiClient
from data_manager import DataManager


data_stock = ApiClient()
data_manager = DataManager()

# Obtain the stock data
result = data_stock.data_request()
# Create the general DF
dataframe = data_stock.dataframe_creation(result)
# Modify the DF so that it contains the variability information
new_dataframe = data_manager.df_with_change()
# Create plot
new_plot = data_manager.plot(new_dataframe)


