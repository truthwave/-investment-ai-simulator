from symbol_fetcher import fetch_symbols
import os

INDEX_SOURCE = os.getenv("INDEX_SOURCE", "sp500")
symbols = fetch_symbols(INDEX_SOURCE)

import csv
from datetime import datetime

def log_signal(symbol, signal_type, price, strategy_name):
    with open("signal_log.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            signal_type,
            price,
            strategy_name  
        ])
