import pandas as pd

def compute_rsi(series, window=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(window=window).mean()
    ma_down = down.rolling(window=window).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_moving_averages(df):
    # 20-DMA (short), 50-DMA (long) for assignment requirement
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    return df

def generate_signals(df):
    # Step 1: Calculate RSI (Assignment: "Implement RSI < 30 as a buy signal")
    df['RSI'] = compute_rsi(df['Close'])

    # Step 2: Calculate 20-DMA and 50-DMA (Assignment: "Confirm with 20-DMA crossing above 50-DMA")
    df = add_moving_averages(df)

    # Step 3: Initialize signals
    df['Signal'] = 0

    # Step 4: Generate buy/sell based on both conditions
    for idx in range(1, len(df)):
        # Buy: RSI < 30 and 20-DMA crosses above 50-DMA (crossover)
        if (
            df['RSI'].iloc[idx] < 30 and
            df['20DMA'].iloc[idx] > df['50DMA'].iloc[idx] and
            df['20DMA'].iloc[idx - 1] <= df['50DMA'].iloc[idx - 1]
        ):
            df.loc[df.index[idx], 'Signal'] = 1  # Buy signal

        # Sell: RSI > 70 and 20-DMA crosses below 50-DMA (optional, for completeness)
        elif (
            df['RSI'].iloc[idx] > 70 and
            df['20DMA'].iloc[idx] < df['50DMA'].iloc[idx] and
            df['20DMA'].iloc[idx - 1] >= df['50DMA'].iloc[idx - 1]
        ):
            df.loc[df.index[idx], 'Signal'] = -1  # Sell signal

    return df
