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
        # Initialize session state for selected stocks if it doesn't exist
        if 'selected_stocks' not in st.session_state:
            st.session_state.selected_stocks = []
        
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
        
    def get_random_date_range(self, max_ipo_year):
        """Generate random 3-year date range starting from max IPO year"""
        yesterday = datetime.today() - timedelta(days=1)
        start_boundary = datetime(max_ipo_year, 1, 1)
        latest_start = yesterday - timedelta(days=180)
        
        if (latest_start - start_boundary).days < 0:
            raise ValueError("Selected stocks' IPO dates are too recent for 3-year analysis")
            
        random_start = start_boundary + timedelta(days=random.randint(0, (latest_start - start_boundary).days))
        random_end = random_start + timedelta(days=180)
        
        return random_start.strftime('%Y-%m-%d'), random_end.strftime('%Y-%m-%d')
        
    def fetch_stock_data(self, selected_tickers, start_date, end_date):
        """Fetch historical data for selected stocks"""
        combined_data = pd.DataFrame()
        
        for ticker in selected_tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date, interval="1wk")
            hist.reset_index(inplace=True)
            hist['Ticker'] = ticker
            combined_data = pd.concat([combined_data, hist])
            
        combined_data.reset_index(inplace=True)
        return combined_data
        
    def fetch_sp500_data(self, start_date, end_date):
        """Fetch S&P 500 data and calculate performance metrics"""
        sp = yf.Ticker('^GSPC')
        data = sp.history(start=start_date, end=end_date, interval="1wk")[['Close']]
        data['returns'] = data['Close'].pct_change()
        data['Percent Change'] = ((data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
        data.reset_index(inplace=True)
        return data
        
    def calculate_portfolio_performance(self, combined_data, selected_tickers):
        """Calculate performance metrics for the portfolio"""
        # Calculate individual stock performance
        for ticker in selected_tickers:
            mask = combined_data['Ticker'] == ticker
            initial_price = combined_data.loc[mask, 'Close'].iloc[0]
            combined_data.loc[mask, 'Percent Change'] = (
                (combined_data.loc[mask, 'Close'] - initial_price) / initial_price * 100
            )
            
        # Calculate portfolio performance
        portfolio_data = combined_data.pivot_table(
            index='Date',
            columns='Ticker',
            values='Percent Change'
        )
        
        num_tickers = len(selected_tickers)
        portfolio_weights = [1/num_tickers] * num_tickers
        portfolio_performance = portfolio_data.mul(portfolio_weights).sum(axis=1)
        
        return pd.DataFrame({
            'Date': portfolio_data.index,
            'Close': portfolio_performance
        })
        
    def create_animation(self, portfolio_data, sp500_data):
        """Create animated performance comparison chart"""
        fig = go.Figure()
        
        # Create animation frames
        frames = [
            go.Frame(
                data=[
                    go.Scatter(x=portfolio_data['Date'][:k+1], 
                              y=portfolio_data['Close'][:k+1], 
                              mode='lines', 
                              name='Portfolio'),
                    go.Scatter(x=sp500_data['Date'][:k+1], 
                              y=sp500_data['Percent Change'][:k+1], 
                              mode='lines',
                              name='S&P500', 
                              line=dict(dash='dot')),
                ],
                name=str(k)
            ) for k in range(len(portfolio_data))
        ]
        
        # Add initial traces
        fig.add_trace(go.Scatter(x=portfolio_data['Date'][:1], 
                                y=portfolio_data['Close'][:1], 
                                mode='lines', 
                                name='Portfolio'))
        fig.add_trace(go.Scatter(x=sp500_data['Date'][:1], 
                                y=sp500_data['Percent Change'][:1], 
                                mode='lines', 
                                name='S&P500', 
                                line=dict(dash='dot')))
        
        # Update layout
        y_min = min(portfolio_data['Close'].min(), sp500_data['Percent Change'].min())
        y_max = max(portfolio_data['Close'].max(), sp500_data['Percent Change'].max())
        
        fig.update_layout(
            xaxis=dict(range=[portfolio_data['Date'].min(), portfolio_data['Date'].max()], 
                      title='Date'),
            yaxis=dict(range=[y_min, y_max], title='Performance (%)'),
            title="Portfolio vs S&P500 Performance",
            updatemenus=[{
                'type': "buttons",
                'showactive': False,
                'buttons': [{
                    'label': "Play",
                    'method': "animate",
                    'args': [None, {
                        "frame": {"duration": 1, "redraw": False},
                        "fromcurrent": True,
                        "mode": "immediate"
                    }]
                }]
            }],
            sliders=[{
                'steps': [{
                    'args': [[str(k)], {
                        "frame": {"duration": 1, "redraw": False},
                        "mode": "immediate"
                    }],
                    'label': str(portfolio_data['Date'].iloc[k].date()),
                    'method': "animate"
                } for k in range(len(portfolio_data))],
                'transition': {"duration": 0},
                'x': 0.1,
                'len': 0.9
            }]
        )
        
        fig.frames = frames
        return fig
        
    def display_performance_metrics(self, portfolio_data, sp500_data, combined_data, selected_tickers):
        """Display performance metrics in expandable sections"""
        with st.expander("Performance Analysis"):
            start_date = sp500_data['Date'].iloc[0].strftime('%Y-%m-%d')
            end_date = sp500_data['Date'].iloc[-1].strftime('%Y-%m-%d')
            
            portfolio_perf = portfolio_data['Close'].iloc[-1]
            sp500_perf = sp500_data['Percent Change'].iloc[-1]
            
            st.write(f"**Analysis Period:** {start_date} to {end_date}")
            st.write(f"**Portfolio Performance:** {portfolio_perf:.2f}%")
            st.write(f"**S&P500 Performance:** {sp500_perf:.2f}%")
            
            st.write("\n**Individual Stock Performance:**")
            for ticker in selected_tickers:
                stock_data = combined_data[combined_data['Ticker'] == ticker]
                initial_value = stock_data['Close'].iloc[0]
                final_value = stock_data['Close'].iloc[-1]
                perf = ((final_value - initial_value) / initial_value) * 100
                st.write(f"{ticker}: {perf:.2f}% (${initial_value:.2f} → ${final_value:.2f})")
    
    def analyze_portfolio(self, selected_stocks):
        """Analyze the selected portfolio for a given period"""
        selected_data = self.df[self.df['name'].isin(selected_stocks)]
        selected_tickers = selected_data['ticker'].tolist()
        max_ipo_year = selected_data['ipo'].max() + 1
        
        # Generate date range and fetch data
        start_date, end_date = self.get_random_date_range(max_ipo_year)
        st.write(f"Analyzing period: {start_date} to {end_date}")
        
        combined_data = self.fetch_stock_data(selected_tickers, start_date, end_date)
        sp500_data = self.fetch_sp500_data(start_date, end_date)
        
        # Calculate portfolio performance
        portfolio_data = self.calculate_portfolio_performance(combined_data, selected_tickers)
        
        # Create and display visualization
        fig = self.create_animation(portfolio_data, sp500_data)
        st.plotly_chart(fig)
        
        # Display performance metrics
        self.display_performance_metrics(portfolio_data, sp500_data, combined_data, selected_tickers)
    
    def run(self):
        """Main application loop"""
        # Create two columns for the selection and refresh button
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Get user input using session state
            selected_stocks = st.multiselect(
                "Select stocks for your portfolio:",
                options=self.df['name'],
                default=st.session_state.selected_stocks
            )
        
        with col2:
            # Add refresh button
            refresh = st.button("New Random Period", key="refresh_period")
        
        if not selected_stocks:
            st.warning("Please select at least one stock to analyze.")
            return
            
        # Update session state
        st.session_state.selected_stocks = selected_stocks
        
        # Analyze portfolio
        self.analyze_portfolio(selected_stocks)

if __name__ == "__main__":
    analyzer = StockAnalyzer()
    analyzer.run()
