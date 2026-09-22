import plotly.express as px
import plotly.graph_objects as go


class PlotlyPlotter:
    def __init__(self, fig):
        self.fig = fig
    def create_line_plot(self, dataframe, column, title):
        fig = px.line(dataframe, y=column, title=title)
        return fig.show()
    def create_multi_line_plot(self,dataframe, column, stock):
        self.fig.add_trace(go.Scatter(
            y=dataframe[column],
            name=stock,
            mode='lines'
        ))





