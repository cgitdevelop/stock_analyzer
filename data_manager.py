"""
Used to create a DataFrame from the data obtained with the API
- It gathers data in a structured way
- It adds new columns with the new calculations to generate the plots
"""


import pandas as pd

class DataManager:
    def dataframe_creation(self, data, stock):
        #Transpose columns
        stock_df = pd.DataFrame(data).T
        #Store in the index the new time objects created
        stock_df.index = pd.to_datetime(stock_df.index)
        #Convert values to float
        stock_df = stock_df.astype(float)
        # Reverse DF
        stock_df = stock_df.sort_index(ascending=True)
        #Rename the column 4. close
        stock_df = stock_df.rename(columns={'4. close': f'{stock} close value'})
        #Convert the index in a column to be used in the animation
        stock_df = stock_df.reset_index().rename(columns={'index': 'Date'})
        return stock_df

    def addition_new_data(self, stock_df, stock):
        # Remove NaN
        stock_df = stock_df.dropna()
        # Calculation of Simple Moving Averages (20 and 50 days)
        stock_df[f'{stock} SMA 20'] = stock_df[f'{stock} close value'].rolling(window=20).mean().round(2)
        stock_df[f'{stock} SMA 50'] = stock_df[f'{stock} close value'].rolling(window=50).mean().round(2)
        # RSI Calculation (14 days)
        delta = stock_df[f'{stock} close value'].diff()
        gain = delta.clip(lower=0)
        loss = -1 * delta.clip(upper=0)
        avg_gain = gain.ewm(com=13, adjust=False).mean()
        avg_loss = loss.ewm(com=13, adjust=False).mean()
        rs = avg_gain / avg_loss
        stock_df[f'{stock} RSI'] = (100 - (100 / (1 + rs))).round(2)

        #Create a new column with normalization
        stock_df[f'{stock} base 100'] = ((stock_df[f'{stock} close value'] / stock_df[f'{stock} close value'].iloc[0]) * 100).round(2)
        #Eliminate nul values resulting from rolling and pct_change
        stock_df = stock_df.dropna().reset_index(drop=True)
        #Create .csv
        stock_df.to_csv(f"{stock}_data.csv")
        return stock_df









