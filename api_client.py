import requests
from dotenv import load_dotenv
import os
import pandas as pd


class ApiClient:
    def __init__(self):
        # Read .env
        load_dotenv()
        # Extract key
        self.api_key = os.getenv("API_KEY_STOCKS")
        self.function = "TIME_SERIES_DAILY"
        self.symbol = "IBM"
        self.datatype = "json"

    def data_request(self):
        parameters_stock = {
            "function": self.function,
            "symbol": self.symbol,
            "datatype": self.datatype,
            "apikey": self.api_key
        }

        response = requests.get(url= "https://www.alphavantage.co/query?", params= parameters_stock)
        data_stocks = response.json()["Time Series (Daily)"]
        return data_stocks

    def dataframe_creation(self, data):
        data_pd = pd.DataFrame(data).T
        df_stock = data_pd.to_csv("stock_data.csv")
        return df_stock
