# plot_profit.py

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("logs/virtual_results.csv")

df = df.dropna(subset=["entry_price", "exit_price"])
df["profit_pct"] = df["profit_pct"].astype(float)
df["balance"] = df["balance"].astype(float)

# グラフ描画
plt.figure(figsize=(10, 5))
plt.bar(df["date"], df["profit_pct"], color=["green" if p > 0 else "red" for p in df["profit_pct"]])
plt.title("Daily Profit (%) - Virtual Backtest")
plt.xlabel("Date")
plt.ylabel("Profit (%)")
plt.axhline(0, color='black', linestyle='--')
plt.tight_layout()
plt.show()

# 統計表示
print("\n📈 日次成績サマリー")
print("平均日利: {:.2f}%".format(df["profit_pct"].mean()))
print("勝率: {:.2f}%".format((df["profit_pct"] > 0).sum() / len(df) * 100))
print("初期資金: 1000 USDT")
print("最終資産: {:.2f} USDT".format(df["balance"].iloc[-1]))
