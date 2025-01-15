import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

class StockAnalyzer:
    def __init__(self):
        self.setup_page()
        self.load_stock_data()
        # Initialize session states
        if 'selected_stocks' not in st.session_state:
            st.session_state.selected_stocks = []
        if 'previous_selection' not in st.session_state:
            st.session_state.previous_selection = []
        if 'submit_clicked' not in st.session_state:
            st.session_state.submit_clicked = False
        
    def setup_page(self):
        """Initialize Streamlit page settings"""
        st.title("Stock Portfolio Performance Analyzer")
        
    def load_stock_data(self):
        """Load initial stock data and tickers"""
        self.stock_data = {
            'name': [
                'Apple', 'Alphabet', 'Microsoft', 'Amazon', 'NVIDIA', 'Meta', 'Tesla',
                'Berkshire Hathaway', 'Eli Lilly', 'Visa', 'Broadcom', 'JPMorgan Chase',
                'UnitedHealth', 'Walmart', 'Mastercard', 'Exxon Mobil', 'Johnson & Johnson',
                'Procter & Gamble', 'Home Depot', 'Costco', 'Chevron', 'Bank of America',
                'Pfizer', 'Walt Disney', 'PayPal', 'Verizon', 'Intel', 'Coca-Cola',
                'Wells Fargo', 'AT&T', 'General Electric', 'Oracle', 'Citigroup', 'IBM',
                'Philip Morris Int.', 'Cisco Systems', 'Merck', 'PepsiCo', 'AIG', 'Amgen',
                'UPS', 'Bristol-Myers Squibb', 'Qualcomm', 'Loews', 'Raytheon', 'McDonalds',
                'Boeing', '3M', 'Altria Group'
            ],
            'ticker': [
                'AAPL', 'GOOG', 'MSFT', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-A', 'LLY', 'V',
                'AVGO', 'JPM', 'UNH', 'WMT', 'MA', 'XOM', 'JNJ', 'PG', 'HD', 'COST', 'CVX',
                'BAC', 'PFE', 'DIS', 'PYPL', 'VZ', 'INTC', 'KO', 'WFC', 'T', 'GE', 'ORCL',
                'C', 'IBM', 'PM', 'CSCO', 'MRK', 'PEP', 'AIG', 'AMGN', 'UPS', 'BMY', 'QCOM',
                'L', 'RTX', 'MCD', 'BA', 'MMM', 'MO'
            ],
            'ipo': [1980, 2004, 1986, 1997, 1999, 2012, 2010, 1965, 1952, 2008, 2009, 1969, 
                    1984, 1970, 2006, 1972, 1944, 1890, 1981, 1985, 1926, 1971, 1942, 1957,
                    2002, 2000, 1971, 1919, 1978, 1984, 1892, 1986, 1986, 1916, 2008, 1990,
                    1970, 1965, 1969, 1983, 1999, 1933, 1991, 1969, 1980, 1965, 1962, 1946, 2008]
        }
        self.df = pd.DataFrame(self.stock_data)

    # [Previous methods remain unchanged: get_random_date_range, fetch_stock_data, 
    # fetch_sp500_data, calculate_portfolio_performance, create_animation, 
    # display_performance_metrics, analyze_portfolio]

    def run(self):
        """Main application loop with delayed refresh"""
        # Create columns for the selection interface
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            # Store the current selection in a temporary variable
            current_selection = st.multiselect(
                "Select stocks for your portfolio:",
                options=self.df['name'],
                default=st.session_state.selected_stocks
            )

        with col2:
            # Add analyze button
            analyze_button = st.button("Analyze Portfolio")

        with col3:
            # Add refresh button for new period
            refresh = st.button("New Random Period")

        # Update the selection only when the analyze button is clicked
        if analyze_button:
            st.session_state.selected_stocks = current_selection
            st.session_state.submit_clicked = True

        # Check if we should display the analysis
        if st.session_state.submit_clicked and st.session_state.selected_stocks:
            if not st.session_state.selected_stocks:
                st.warning("Please select at least one stock to analyze.")
                return
            
            # Analyze portfolio
            self.analyze_portfolio(st.session_state.selected_stocks)
        elif not st.session_state.selected_stocks:
            st.info("Select stocks and click 'Analyze Portfolio' to see the analysis.")

if __name__ == "__main__":
    analyzer = StockAnalyzer()
    analyzer.run()