# analyze_trades.py

import pandas as pd

def analyze_trade_log(filename="trade_log.csv"):
    df = pd.read_csv(filename)

    total_trades = len(df)
    wins = df[df["pnl"] > 0]
    losses = df[df["pnl"] <= 0]
    win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0

    print(f"総取引数: {total_trades} 回")
    print(f"勝率: {win_rate:.2f}%")
    print(f"平均利益: {wins['pnl'].mean():.2f}円")
    print(f"平均損失: {losses['pnl'].mean():.2f}円")
    print(f"最大利益: {wins['pnl'].max():.2f}円")
    print(f"最大損失: {losses['pnl'].min():.2f}円")
    print(f"合計損益: {df['pnl'].sum():.2f}円")

if __name__ == '__main__':
    analyze_trade_log()
