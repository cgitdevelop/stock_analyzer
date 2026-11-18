"""
Used to generate de plots
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


class PlotlyPlotter:
    def __init__(self, fig):
        self.fig = fig

    def create_static_dashboard(self, df, stock):
        # 1. Extract start and end dates from DataFrame
        start_date = df['Date'].min().strftime('%Y-%m-%d')
        end_date = df['Date'].max().strftime('%Y-%m-%d')

        # 2. Create 1x2 layout (50% width each)
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.5, 0.5],
            subplot_titles=(
                f"{stock} - Trend (Price and Moving Averages)",
                f"{stock} - Momentum (RSI 14)"
            )
        )

        # 3. Left Panel (row=1, col=1): Price and Moving Averages
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df[f'{stock} close value'], name="Close Price", mode="lines",
                       line=dict(color="white", width=2)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df[f'{stock} SMA 20'], name="SMA 20", mode="lines",
                       line=dict(color="cyan", dash="dot")),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df[f'{stock} SMA 50'], name="SMA 50", mode="lines",
                       line=dict(color="orange", dash="dash")),
            row=1, col=1
        )

        # 4. Right Panel (row=1, col=2): Momentum (RSI)
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df[f'{stock} RSI'], name="RSI (14)", mode="lines", line=dict(color="magenta")),
            row=1, col=2
        )

        # RSI threshold lines (30 and 70)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=1, col=2, annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="lightgreen", row=1, col=2, annotation_text="Oversold")

        # 5. Layout configuration (height adjusted for a single row)
        fig.update_layout(
            title_text=f"{stock} Analysis (Period: {start_date} to {end_date})",
            height=450,
            template="plotly_dark"
        )
        return fig


    def create_multi_line_plot(self,dataframe, column, stock):
        self.fig.add_trace(go.Scatter(
            y=dataframe[column],
            name=stock,
            mode='lines'
        ))






