# create_sample_csv.py

import pandas as pd

# ダミーデータの生成（中期成長株の条件を含むものと含まないものを混在）
data = [
    {"ティッカー": "AAPL", "売上成長率": 12.5, "EPS成長率": 15.0, "PER": 28, "ROE": 18},
    {"ティッカー": "MSFT", "売上成長率": 9.8, "EPS成長率": 8.5, "PER": 32, "ROE": 14},
    {"ティッカー": "TSLA", "売上成長率": 30.2, "EPS成長率": 40.1, "PER": 25, "ROE": 20},
    {"ティッカー": "AMZN", "売上成長率": 5.0, "EPS成長率": 6.0, "PER": 60, "ROE": 7},
    {"ティッカー": "NVDA", "売上成長率": 35.0, "EPS成長率": 50.0, "PER": 27, "ROE": 30},
]

df = pd.DataFrame(data)

# CSVファイルとして保存
df.to_csv("stocks.csv", index=False, encoding="utf-8-sig")

print("✅ stocks.csv を作成しました。")
