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

st.set_page_config(layout="wide") #Wide layout for dashboard
st.title("My stock analyzer")

#Cache code
@st.cache_data(ttl=86400, show_spinner="Descargando datos de la API...") #it states 1 day of cache, and adds a message
def fetch_stock_data(stock):
    #Instantiates the class and queries the data
    data_stock = ApiClient(stock)
    return data_stock.data_request()



#User query for getting stock names
user_query = st.text_input("Which stocks do you want to analyze? (separated by commas)")
if user_query:
    list_stocks = [stock.strip().upper() for stock in user_query.split(',')]


    if st.button("Analyze"):
        data_manager = DataManager()

        #Initialize multi-stock plot if there are multiple stocks
        if len(list_stocks) > 1:
            fig_master = go.Figure()
            fig_master.update_layout(
                title_text="Performance Comparison (Base 100)",
                template="plotly_dark",
                height=500
            )
            space_base_100 = st.empty()
            st.divider()
            plotly_plot_master = PlotlyPlotter(fig_master)

        for stock in list_stocks:

        ### Download of data from API ###
            #Gets data using the function created
            api_data = fetch_stock_data(stock)
            # Check if too many queries used
            if api_data is None:
                st.error("Stopping process due to excess of API requests")
                break

        ### Creation of the dataframe ###
            # Create df
            stock_df = data_manager.dataframe_creation(api_data, stock)
            # Add variation column
            df_new_column = data_manager.addition_new_data(stock_df, stock)

        ### Plotting ###
            #Add data in plot Base 100
            if len(list_stocks) > 1:
                plotly_plot_master.create_multi_line_plot(df_new_column, f'{stock} base 100', stock)
                space_base_100.plotly_chart(fig_master, use_container_width=True)

            #Render of individual plot
            fecha_inicio = df_new_column['Date'].min().strftime('%Y-%m-%d')
            fecha_fin = df_new_column['Date'].max().strftime('%Y-%m-%d')

            st.subheader(f"Individual Analysis: {stock}")
            st.text(f"Data period: {fecha_inicio} to {fecha_fin}")

            plotly_plot_ind = PlotlyPlotter(None)
            fig_dashboard = plotly_plot_ind.create_static_dashboard(df_new_column, stock)
            st.plotly_chart(fig_dashboard, use_container_width=True)





