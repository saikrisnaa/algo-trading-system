import logging
from datetime import datetime
import pandas as pd
import schedule
import time
from data_fetcher import fetch_data
from trading_strategy import generate_signals
from ml_model import ml_decision_tree  
from google_sheets import update_worksheet_with_df
from telegram_alerts import send_telegram_message

logging.basicConfig(level=logging.INFO, filename="trading.log", force=True)

STOCKS = ['RELIANCE.NS', 'ICICIBANK.NS', 'HDFCBANK.NS']

def process_trades(all_trades_df):
    if all_trades_df.empty:
        return pd.DataFrame(), pd.DataFrame(), 0

    trade_log = []
    win_count = 0
    loss_count = 0
    
    for ticker in all_trades_df['Ticker'].unique():
        ticker_trades = all_trades_df[all_trades_df['Ticker'] == ticker].sort_values(by='Date').reset_index()
        open_position = False
        entry_price = 0
        
        for index, trade in ticker_trades.iterrows():
            if trade['Type'] == 'BUY' and not open_position:
                open_position = True
                entry_price = trade['Price']
            
            elif trade['Type'] == 'SELL' and open_position:
                exit_price = trade['Price']
                pnl = exit_price - entry_price
                pnl_percent = (pnl / entry_price) * 100
                
                if pnl > 0:
                    win_count += 1
                else:
                    loss_count += 1
                
                trade_log.append({
                    'Ticker': ticker,
                    'Entry Date': ticker_trades.loc[index-1, 'Date'] if index > 0 else 'N/A',
                    'Entry Price': entry_price,
                    'Exit Date': trade['Date'],
                    'Exit Price': exit_price,
                    'P&L': pnl,
                    'P&L %': pnl_percent
                })
                open_position = False

    total_trades = win_count + loss_count
    win_ratio = (win_count / total_trades) * 100 if total_trades > 0 else 0

    trade_log_df = pd.DataFrame(trade_log)
    summary_df = pd.DataFrame({
        'Metric': ['Total Trades', 'Winning Trades', 'Losing Trades', 'Win Ratio (%)'],
        'Value': [total_trades, win_count, loss_count, f"{win_ratio:.2f}"]
    })
    
    return trade_log_df, summary_df

def run_algo():
    logging.info(f"Running algo at {datetime.now()}")
    
    all_trades = []
    data = fetch_data(STOCKS)
    
    for ticker, df in data.items():
        # Run the ML model on the historical data for each stock
        acc, _ = ml_decision_tree(df.copy()) 
        logging.info(f"{ticker}: ML accuracy {acc}")
        print(f"{ticker}: ML accuracy {acc}")

        df_with_signals = generate_signals(df)
        
        # Collect all trades from the backtest
        for index, row in df_with_signals[df_with_signals['Signal'] != 0].iterrows():
            trade_type = "BUY" if row['Signal'] == 1 else "SELL"

            alert_message = (
            f"*Trade Signal Found!*\n\n"
            f"*Ticker:* {ticker}\n"
            f"*Type:* {trade_type}\n"
            f"*Date:* {index.strftime('%Y-%m-%d')}\n"
            f"*Price:* {row['Close']:.2f}"
            )
            send_telegram_message(alert_message)

            all_trades.append({
                'Date': index.strftime('%Y-%m-%d'),
                'Ticker': ticker,
                'Type': trade_type,
                'Price': row['Close']
            })

    if not all_trades:
        print("No trades were found across all stocks in the backtest period.")
        return

    # Creates a DataFrame from the collected trades
    all_trades_df = pd.DataFrame(all_trades)
    
    # Process the trades to get P&L and summary stats
    trade_log_df, summary_df = process_trades(all_trades_df)

    # Writing all results to Google Sheets
    update_worksheet_with_df('Trading-system', 'All Signals', all_trades_df)
    update_worksheet_with_df('Trading-system', 'Trade P&L Log', trade_log_df)
    update_worksheet_with_df('Trading-system', 'Summary', summary_df)

if __name__ == "__main__":
    #run_algo()
    schedule.every().day.at("10:30").do(run_algo)
    logging.info("Scheduler started")
    print("Scheduler started. Waiting for the scheduled job ...")
    while True:
        schedule.run_pending()
        time.sleep(1) # Sleep to avoid busy-waiting