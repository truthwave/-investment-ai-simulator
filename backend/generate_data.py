import os
import pandas as pd
import numpy as np

# 1年分（365日）の高ボラティリティな1時間足データを生成
np.random.seed(42)
hours = 24 * 365
timestamps = pd.date_range("2023-01-01", periods=hours, freq="H")

base_price = 25000
price_changes = np.random.normal(loc=0, scale=100, size=hours).cumsum()
close_prices = base_price + price_changes
highs = close_prices + np.random.uniform(50, 150, size=hours)
lows = close_prices - np.random.uniform(50, 150, size=hours)
opens = close_prices + np.random.uniform(-50, 50, size=hours)
volumes = np.random.randint(1000, 10000, size=hours)

df = pd.DataFrame({
    "timestamp": timestamps,
    "open": opens,
    "high": highs,
    "low": lows,
    "close": close_prices,
    "volume": volumes
})

# 保存先のフォルダを作成
os.makedirs("data", exist_ok=True)

# CSVとして保存
df.to_csv("data/historical_price.csv", index=False)
print("✅ data/historical_price.csv を作成しました")
