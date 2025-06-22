# fetch_binance_data.py

import requests
import pandas as pd
import time
import datetime

def fetch_ohlcv(symbol, interval, start_str, end_str=None, limit=1000):
    base_url = 'https://api.binance.com/api/v3/klines'
    start_ts = int(pd.to_datetime(start_str).timestamp() * 1000)
    end_ts = int(pd.to_datetime(end_str).timestamp() * 1000) if end_str else None

    all_data = []
    while True:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_ts,
            'limit': limit
        }
        if end_ts:
            params['endTime'] = end_ts

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print("取得失敗", response.text)
            break

        data = response.json()
        if not data:
            break

        all_data.extend(data)
        start_ts = data[-1][0] + 1  # 次のローソク足へ
        time.sleep(0.3)

        # 終端チェック
        if len(data) < limit:
            break

    df = pd.DataFrame(all_data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_base_volume", "taker_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
    return df

# ===== 実行パート =====

if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "1d"  # 変更可：1m, 5m, 1h, 1dなど
    start_date = "2019-01-01"
    today = datetime.date.today().strftime("%Y-%m-%d")

    df = fetch_ohlcv(symbol, interval, start_date, today)
    df.to_csv("btc_price_data_1d.csv", index=False)
    print(f"✅ {len(df)}本のデータを保存しました: btc_price_data_1d.csv")
