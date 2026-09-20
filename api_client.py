import requests
from dotenv import load_dotenv
import os


class ApiClient:
    def __init__(self, symbol):
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

        response = requests.get(url= "https://www.alphavantage.co/query?", params= parameters_stock)
        json_response = response.json()
        if "Information" in json_response:
            return None
        else:
            data_stock = json_response["Time Series (Daily)"]
            return data_stock


