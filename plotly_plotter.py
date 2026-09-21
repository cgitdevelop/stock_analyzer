import plotly.express as px


class PlotlyPlotter:
    def create_plot_plotly(self, dataframe, column):
        fig = px.line(dataframe, y=column)
        return fig.show()





