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
        return stock_df

    def addition_new_data(self, stock_df, stock):
        # Remove NaN
        stock_df = stock_df.dropna()
        #Create new column with tendency data
        stock_df[f'{stock} moving average'] = (stock_df[f'{stock} close value'].rolling(window=20).mean()).round(2)
        # Calculation pct_daily_change and Round to 2 decimals
        stock_df[f'{stock} pct daily change'] = (stock_df[f'{stock} close value'].pct_change() * 100).round(2)
        #Create a new column with normalization
        stock_df[f'{stock} base 100'] = ((stock_df[f'{stock} close value'] / stock_df[f'{stock} close value'].iloc[0]) * 100).round(2)
        #Create .csv
        stock_df.to_csv(f"{stock}_data.csv")
        return stock_df









