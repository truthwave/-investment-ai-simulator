# daily_summary.py

import pandas as pd
import matplotlib.pyplot as plt

def summarize_by_day(csv_file="trade_log.csv"):
    df = pd.read_csv(csv_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # 日次損益集計
    daily = df.groupby("date")["pnl"].agg(["count", "sum", "mean"])
    daily.rename(columns={"count": "trades", "sum": "total_pnl", "mean": "avg_pnl"}, inplace=True)

    # 累積損益の追加
    daily["cumulative_pnl"] = daily["total_pnl"].cumsum()

    # 表示
    print("=== 日次サマリー ===")
    print(daily)

    # グラフ作成（累積損益）
    plt.figure(figsize=(10, 5))
    plt.plot(daily.index, daily["cumulative_pnl"], marker='o', color='green', label='累積損益')
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.xlabel("日付")
    plt.ylabel("損益 (円)")
    plt.title("累積損益グラフ")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cumulative_pnl_graph.png")
    plt.show()

if __name__ == "__main__":
    summarize_by_day()
