import os
import pandas as pd
from binance.client import Client
import pandas as pd
import datetime

# Binance APIキーとシークレットキーを設定
api_key = 'your_api_key'      # ここにあなたのAPIキーを入力してください
api_secret = 'your_api_secret'  # ここにあなたのシークレットキーを入力してください

client = Client(api_key, api_secret)

# 通貨ペアと時間間隔を設定
symbol = 'BTCUSDT'  # 例：ビットコインとテザーのペア
interval = Client.KLINE_INTERVAL_1DAY  # 1日の間隔

# 開始日と終了日を設定
start_str = '2023-01-01'  # データ取得開始日
end_str = '2023-12-31'    # データ取得終了日

# データを取得
klines = client.get_historical_klines(symbol, interval, start_str, end_str)

# データをデータフレームに変換
df = pd.DataFrame(klines, columns=[
    'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
    'Close Time', 'Quote Asset Volume', 'Number of Trades',
    'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
])

# タイムスタンプを日時に変換
df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

# 数値データを適切な型に変換
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume',
                   'Quote Asset Volume', 'Number of Trades',
                   'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']
df[numeric_columns] = df[numeric_columns].astype(float)

# CSVファイルとして保存
df.to_csv('historical_data.csv', index=False)

print("データの取得と保存が完了しました。")
