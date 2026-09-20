import pandas as pd

class DataManager:
    def dataframe_creation(self, data, stock):
        #Transpose columns
        data_pandas = pd.DataFrame(data).T
        #Create csv
        data_pandas.to_csv(f"{stock}_data.csv")
        #Create dataframe for stock
        stock_df = pd.read_csv(f"{stock}_data.csv", index_col=0)
        #Convert index to datetime
        stock_df.index = pd.to_datetime(stock_df.index)
        #Reverse DF
        stock_df = stock_df.sort_index(ascending=True)
        return stock_df

    def daily_variation_addition(self, stock_df, stock):
        #Calculation of all pct_daily_change
        stock_df[f'{stock}_pct_daily_change'] = stock_df['4. close'].pct_change() * 100
        #Round to 2 decimals and eliminate NaN
        stock_df[f'{stock}_pct_daily_change'] = round(stock_df[f'{stock}_pct_daily_change'], 2)
        #Remove NaN
        stock_df = stock_df.dropna()
        return (stock_df)









