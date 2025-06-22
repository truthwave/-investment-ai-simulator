# data_loader.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_price_data(symbol, timeframe):
    # ダミーの1週間分のデータ生成（1時間足）
    now = datetime.now()
    dates = [now - timedelta(hours=i) for i in range(7*24)]
    dates.reverse()

    prices = []
    price = 50000
    for _ in range(7 * 24):
        change = np.random.randn() * 100
        high = price + abs(change)
        low = price - abs(change)
        close = price + change
        prices.append((high, low, close))
        price = close

    df = pd.DataFrame(prices, columns=["high", "low", "close"])
    df["datetime"] = dates
    return df
