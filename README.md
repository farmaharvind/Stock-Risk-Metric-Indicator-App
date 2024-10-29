# Stock Analysis Web App

A Flask-based web application that provides financial analysis of stocks using data from Yahoo Finance. Enter any stock ticker to get detailed performance metrics, comparative analysis against the S&P 500, and visualizations of recent price movements.

## Features

- **Real-Time Stock Data**: Fetch current and historical stock prices using Yahoo Finance API
- **Comprehensive Analysis**: Calculate key metrics including:
  - Alpha and Beta
  - R-squared value
  - Sharpe Ratio
  - Standard Deviation
  - Historical Returns
- **Visual Analytics**: 
  - 30-day performance charts
  - Price trend visualization
  - Benchmark comparison plots
- **Market Comparison**: Automatic comparison against S&P 500 performance
- **User-Friendly Interface**: Simple input field for stock tickers with clear result display

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/stock-analysis-app.git
    cd stock-analysis-app
    ```

2. Create and activate a virtual environment (recommended):
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install required packages:
    ```
    pip install -r requirements.txt
    ```

## Dependencies

Create a `requirements.txt` file with the following dependencies:

    Flask==2.0.1
    yfinance==0.1.70
    pandas==1.3.3
    numpy==1.21.2
    matplotlib==3.4.3
    pytz==2021.3

## Usage

1. Start the Flask server:
    ```
    python app.py
    ```

2. Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

3. Enter a stock ticker (e.g., AAPL, GOOGL, MSFT) in the input field

4. View the generated analysis including:
    - Recent price data
    - Performance metrics
    - Comparison with S&P 500
    - Visual charts and graphs

## Project Structure

    stock-analysis-app/
    ├── app.py              # Main Flask application
    ├── static/
    │   ├── css/           # Stylesheet files
    │   └── js/            # JavaScript files
    ├── templates/
    │   ├── index.html     # Main page template
    │   └── analysis.html  # Results template
    ├── requirements.txt    # Project dependencies
    └── README.md          # This file

## Key Components

### Data Processing Functions

- `fetch_stock_data(ticker)`: Retrieves historical stock data
- `calculate_metrics(data, benchmark)`: Computes financial metrics
- `generate_plots(stock_data)`: Creates visualization charts

### Routes

- `GET /`: Main page with input form
- `POST /analyze`: Processes stock ticker and returns analysis
- `GET /history/<ticker>`: Returns historical data for a stock

## Error Handling

The application includes robust error handling for:
- Invalid stock tickers
- API connection issues
- Data processing errors
- Missing or incomplete data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Create Pull Request

## Troubleshooting

### Common Issues

1. **No Data Retrieved**
    - Verify the stock ticker is valid
    - Check your internet connection
    - Ensure Yahoo Finance API is accessible

2. **Visualization Errors**
    - Confirm matplotlib is properly configured
    - Check if `Agg` backend is set for non-interactive environments

3. **Performance Issues**
    - Consider implementing data caching
    - Optimize database queries if applicable
    - Reduce the amount of historical data being processed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Yahoo Finance for providing stock data
- Flask framework developers
- Contributors to the pandas and numpy libraries
