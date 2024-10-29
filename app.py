from flask import Flask, request, render_template
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import pytz


app = Flask(__name__)

RISK_FREE_RATE = 0.03
BENCHMARK_TICKER = "^GSPC"

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    benchmark = yf.Ticker(BENCHMARK_TICKER)
    company_name = stock.info.get('longName', 'N/A')
    end_date = datetime.today().astimezone(pytz.UTC)
    start_date = end_date - timedelta(days=3*365 + 50)
    
    stock_data = stock.history(start=start_date, end=end_date, interval='1d')
    benchmark_data = benchmark.history(start=start_date, end=end_date, interval='1d')

    if stock_data.empty or benchmark_data.empty:
        return None, None, None, None, None

    stock_data['Returns'] = stock_data['Close'].pct_change() * 100
    stock_data['Returns'] = stock_data['Returns'].round(2)
    stock_data.dropna(inplace=True)
    benchmark_data['Returns'] = benchmark_data['Close'].pct_change()
    benchmark_data.dropna(inplace=True)

    stock_metrics = calculate_metrics(stock_data, benchmark_data, RISK_FREE_RATE)
    benchmark_metrics = calculate_metrics(benchmark_data, benchmark_data, RISK_FREE_RATE)

    last_5_days = stock_data.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume', 'Returns']]
    last_5_days.index = last_5_days.index.strftime('%Y-%m-%d')

    stock_30d_return = (stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-30]) / stock_data['Close'].iloc[-30] * 100
    benchmark_30d_return = (benchmark_data['Close'].iloc[-1] - benchmark_data['Close'].iloc[-30]) / benchmark_data['Close'].iloc[-30] * 100
    performance_difference = round(stock_30d_return - benchmark_30d_return, 2)
    comparison_text = f"{'Outperformed' if performance_difference > 0 else 'Underperformed'} the S&P 500 by {abs(performance_difference)}% over the last 30 days."

    # Generate 30-day stock-only plot
    stock_plot_url = generate_comparison_plot(stock_data['Close'].tail(30))

    metrics = {
        'Company Name': company_name,
        'Stock Metrics': stock_metrics,
        'Benchmark Metrics': benchmark_metrics
    }
    
    return company_name, last_5_days, metrics, stock_plot_url, comparison_text

def calculate_metrics(data, benchmark_data, risk_free_rate):
    aligned_data = data['Returns'].align(benchmark_data['Returns'], join='inner')
    data_returns, benchmark_returns = aligned_data[0], aligned_data[1]

    covariance = np.cov(data_returns, benchmark_returns)[0, 1]
    variance = np.var(benchmark_returns)
    beta = covariance / variance

    avg_stock_return = data_returns.mean() * 252
    avg_benchmark_return = benchmark_returns.mean() * 252
    alpha = avg_stock_return - (risk_free_rate + beta * (avg_benchmark_return - risk_free_rate))
    
    correlation = data_returns.corr(benchmark_returns)
    r_squared = correlation ** 2
    std_dev = data_returns.std() * np.sqrt(252)
    sharpe_ratio = (avg_stock_return - risk_free_rate) / std_dev
    
    explanations = {
        'Alpha': {'value': round(alpha, 4), 'text': f"{'Positive' if alpha > 0 else 'Negative'} alpha indicates {'outperformance' if alpha > 0 else 'underperformance'} relative to the benchmark.", 'color': 'green' if alpha > 0 else 'red'},
        'Beta': {'value': round(beta, 4), 'text': f"A beta of {round(beta, 4)} suggests that the stock is {'more' if beta > 1 else 'less'} volatile than the benchmark.", 'color': 'green' if beta <= 1 else 'red'},
        'R-Squared': {'value': round(r_squared, 4), 'text': f"An R-squared of {round(r_squared * 100, 2)}% indicates the percentage of the stock’s movement explained by the benchmark.", 'color': 'green' if r_squared > 0.7 else 'red'},
        'Standard Deviation': {'value': round(std_dev, 4), 'text': f"A higher standard deviation ({round(std_dev, 4)}) implies greater volatility in the stock's returns.", 'color': 'red' if std_dev > 0.2 else 'green'},
        'Sharpe Ratio': {'value': round(sharpe_ratio, 4), 'text': f"A Sharpe Ratio of {round(sharpe_ratio, 4)} {'indicates good risk-adjusted return' if sharpe_ratio > 1 else 'suggests lower risk-adjusted return'}.", 'color': 'green' if sharpe_ratio > 1 else 'red'}
    }

    return explanations

# Function to generate a stock-only plot for the last 30 days
def generate_comparison_plot(stock_data):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data, label='Stock', marker='o', color='b')
    plt.title('30-Day Stock Performance')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{plot_url}'

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    company_name = None
    metrics = None
    stock_plot_url = None
    comparison_text = None
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        company_name, data, metrics, stock_plot_url, comparison_text = fetch_stock_data(ticker)
        if data is None:
            data = f"No data found for ticker {ticker}."
        else:
            data = data.to_html(classes='table table-striped')
    return render_template('index.html', data=data, company_name=company_name, metrics=metrics, stock_plot_url=stock_plot_url, comparison_text=comparison_text)

if __name__ == '__main__':
    app.run(debug=True)
