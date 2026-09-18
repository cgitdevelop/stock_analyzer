import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class DataManager:
    def df_with_change(self):
        # Read DF created and add dates as index
        self.dataframe = pd.read_csv("stock_data.csv", index_col=0)
        # Convert index to datetime
        self.dataframe.index = pd.to_datetime(self.dataframe.index)
        # Reverse DF
        self.dataframe = self.dataframe.sort_index(ascending=True)
        # Calculation of all pct_daily_change
        self.dataframe['pct_daily_change'] = self.dataframe['4. close'].pct_change() * 100
        # Round to 2 decimals and eliminate NaN
        self.dataframe['pct_daily_change'] = round(self.dataframe['pct_daily_change'], 2)
        self.dataframe = self.dataframe.dropna()
        return (self.dataframe['pct_daily_change'])

    def plot(self, dataframe):
        # Create plot
        self.dataframe['pct_daily_change'].plot(title="Daily evolution (%)", color="blue", figsize=(10, 5))
        ax = plt.gca()
        # We add interval of 5 days
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        # We add text format
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.xlabel("Days")
        plt.ylabel("Daily variation (%)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("Daily_evolution.png")
        plt.close()






