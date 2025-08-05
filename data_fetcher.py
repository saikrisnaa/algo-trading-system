import yfinance as yf
import pandas as pd
import time

def fetch_data(tickers):
    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="max", interval="1d", progress = False, auto_adjust = True)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
            df.sort_index(inplace=True)
            data[ticker] = df
            print(f"{ticker} clean columns: {df.columns}")
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return data
