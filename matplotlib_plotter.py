import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class MatplotlibPlotter:
    def add_line(self, stock_df, column, stock):
        stock_df[column].plot(label=stock)

    def save_plot(self, title):
        plt.title(title)
        ax = plt.gca()
        # We add interval of 5 days
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        # We add format
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.xlabel("Days")
        plt.ylabel(title)
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{title}.png")
        plt.close()






