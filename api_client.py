import pandas as pd
import requests
from dotenv import load_dotenv
import json
import os


class ApiClient:
    def __init__(self, symbol):
        #Variable to avoid using API for testing
        self.no_api = 1 # 1 to avoid API
        # Read .env
        load_dotenv()
        # Extract key
        self.api_key = os.getenv("API_KEY_STOCKS")
        self.function = "TIME_SERIES_DAILY"
        self.symbol = symbol
        self.datatype = "json"

    def data_request(self):
        parameters_stock = {
            "function": self.function,
            "symbol": self.symbol,
            "datatype": self.datatype,
            "apikey": self.api_key
        }

        if self.no_api == 1:
            with open('json_IBM_file.json', 'r') as file:
                json_response = json.load(file)
                return json_response["Time Series (Daily)"]
        else:
            response = requests.get(url= "https://www.alphavantage.co/query?", params= parameters_stock)
            json_response = response.json()
            if "Information" in json_response:
                return None
            else:
                data_stock = json_response["Time Series (Daily)"]
            return data_stock