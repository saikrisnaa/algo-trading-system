# Algo Trading System with ML and Automation
This is a Python-based prototype of an algo trading system. The system connects to a stock data API, implements a quantitative trading strategy, backtests its performance, and automates the logging and analysis of results to Google Sheets, with real-time alerts sent via Telegram.

## Key Features

- Automated Data Ingestion: Fetches daily historical stock data for multiple NIFTY 50 tickers using the yfinance API.
- Quantitative Trading Strategy: Implements a trading strategy based on a combination of two technical indicators:

Buy Signal is generated when the 14-day RSI is below 30 (oversold).
This signal is confirmed only when the 20-Day Moving Average crosses above the 50-Day Moving Average.

- Historical Backtesting: The system automatically backtests the trading strategy over the entire available history of the stocks to find all valid trade signals.

- Machine Learning Integration: A Decision Tree classifier is used to predict the next day's stock price movement based on indicators like RSI, Moving Averages, and Volume. The model's prediction accuracy is logged for each run.

- Google Sheets Automation: Automatically logs all trade signals, a calculated Profit & Loss summary, and the strategy's win ratio to a Google Sheet.

- The report is organized into three distinct tabs for clarity:
All Signals, Trade P&L Log, and Summary.

- Scheduled Automation: The entire workflow is encapsulated in a single function that can be scheduled to run automatically at a set time every day.

- Telegram Alerts: The system provides real-time notifications for every new trade signal via a custom Telegram bot, enabling instant updates.

- Modular and Robust Code: The codebase is organized into logical modules for data fetching, strategy, ML, and reporting, and includes logging for monitoring and debugging.

## Tech Stack
- Python
- Pandas
- yfinance
- scikit-learn
- gspread and gspread-dataframe
- schedule
- requests

## Setup and Installation
Follow these steps to set up and run the project locally.

1. Clone the Repository

2. Create and Activate a Virtual Environment

3. Install Dependencies
   With the help of requirements.txt, install all the dependencies from the file

4. Configure Google Sheets API
   Follow the Google Cloud documentation to create a service account and enable the Google Sheets and Google Drive APIs.

Download the JSON key file for the service account.

Rename the file to credentials.json and place it in the root directory of this project.

Share your target Google Sheet with the client_email found inside your credentials.json file.

5. Configure Telegram Bot
   Open the telegram_alerts.py file.

Replace the placeholder values for BOT_TOKEN and CHAT_ID with your own credentials.

## Run the application

- To run the application enter this command in terminal - python main.py
- The script will now wait and execute automatically at the scheduled time, print the ML accuracy to the console, and update the Google Sheet.

