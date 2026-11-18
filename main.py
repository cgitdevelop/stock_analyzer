"""
Script to analyze history of stocks
- Executed with "streamlit run main.py"
- User will introduce the stock symbols
- API is used to get stock data with ApiClient()
- DataManager is used to gather the data as a DF
- PlotlyPlotter is used to create the plots
"""



from api_client import ApiClient
from data_manager import DataManager
from plotly_plotter import PlotlyPlotter
import plotly.graph_objects as go
import time
import streamlit as st


st.title("My stock analyzer")


#User query for getting stock names
user_query = st.text_input("Which stocks do you want to analyze? (separated by commas)")
if user_query:
    list_stocks = [stock.strip().upper() for stock in user_query.split(',')]


#Flow to ask for individual plots
    show_individual = False
    if len(list_stocks) == 1:
        show_individual = True
    else:
        individual_stock = st.radio("Besides the multi-stock comparison, do you want to see individual plots for these stocks?", options= ["Yes", "No"])

        if individual_stock == 'Yes':
            show_individual = True


    if st.button("Analyze"):
        fig = go.Figure()
        #Add title to multi-stock plot
        fig.update_layout(title_text="Performance Comparison (Base 100)")
        # Block space for base100 plot
        space_base_100 = st.empty()
        # Add dividers
        st.divider()

        data_manager = DataManager()
        plotly_plot = PlotlyPlotter(fig)

        for stock in list_stocks:
        ### Download of data from API ###
            data_stock = ApiClient(stock)
            #Obtain stock data
            api_data = data_stock.data_request()
            # Check if too many queries used
            if api_data is None:
                st.error("Stopping process due to excess of API requests")
                break

        ### Creation of the dataframe ###
            #Create df
            stock_df = data_manager.dataframe_creation(api_data,stock)
            #Add variation column
            df_new_column = data_manager.addition_new_data(stock_df,stock)

        ### Plotting ###
            if show_individual:
                #Principal plot: Closing + MA
                fig_tendency = plotly_plot.create_line_plot(df_new_column, [f'{stock} close value', f'{stock} moving average'], f'1. {stock} - Tendency and daily values')
                st.plotly_chart(fig_tendency)
                #Secondary plot: Daily change (Volatility)
                fig_daily = plotly_plot.create_line_plot(df_new_column, f'{stock} pct daily change', f'2. {stock} - Daily variation (volatility)')
                st.plotly_chart(fig_daily)
            if len(list_stocks) > 1:
                # Principal plot: Base 100 for all stocks
                plotly_plot.create_multi_line_plot(df_new_column, f'{stock} base 100', stock)
                space_base_100.plotly_chart(fig)
            time.sleep(15)




