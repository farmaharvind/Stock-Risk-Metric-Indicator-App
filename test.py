import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Function to fetch stock data and calculate technical indicators
def fetch_stock_data(ticker):
    # Define the start and end date with a buffer of 50 extra days for indicator calculation
    end_date = datetime.today().astimezone(pytz.UTC)  # Make end_date timezone-aware
    start_date = end_date - timedelta(days=3*365 + 50)
    
    # Download historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    
    # Check if data is available
    if stock_data.empty:
        print(f"No data found for {ticker}.")
        return None
    
    # Calculate Simple and Exponential Moving Averages
    stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['EMA_20'] = stock_data['Close'].ewm(span=20, adjust=False).mean()
    
    # Calculate Relative Strength Index (RSI)
    delta = stock_data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate Bollinger Bands
    rolling_mean = stock_data['Close'].rolling(window=20).mean()
    rolling_std = stock_data['Close'].rolling(window=20).std()
    stock_data['Bollinger_Mid'] = rolling_mean
    stock_data['Bollinger_Upper'] = rolling_mean + (2 * rolling_std)
    stock_data['Bollinger_Lower'] = rolling_mean - (2 * rolling_std)
    
    # Calculate MACD (Moving Average Convergence Divergence)
    stock_data['MACD'] = stock_data['Close'].ewm(span=12, adjust=False).mean() - stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    
    # Calculate Average True Range (ATR)
    high_low = stock_data['High'] - stock_data['Low']
    high_close = (stock_data['High'] - stock_data['Close'].shift()).abs()
    low_close = (stock_data['Low'] - stock_data['Close'].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    stock_data['ATR'] = true_range.rolling(window=14).mean()
    
    # Filter data to keep only the last 3 years
    stock_data = stock_data.loc[end_date - timedelta(days=3*365):]

    # Display first few rows of the filtered data
    print(stock_data.head())
    
    # Return the data for further processing or storage
    return stock_data

# Example usage
ticker = "AAPL"  # Replace with any ticker symbol
data = fetch_stock_data(ticker)
