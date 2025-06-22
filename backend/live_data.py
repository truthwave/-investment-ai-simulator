import yfinance as yf
import pandas as pd
import os

# 監視する銘柄リスト
tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
s
# 保存先ディレクトリ
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

def fetch_and_save_data():
    """Yahoo Finance APIからデータを取得し、CSVに保存"""
    all_data = []

    for ticker in tickers:
        print(f"📡 {ticker} のデータを取得中...")
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="8d", interval="1m")  # 1分足データを取得

            if data.empty:
                print(f"⚠ {ticker} のデータが見つかりませんでした。")
                continue

            data["Ticker"] = ticker
            all_data.append(data)
            print(f"✅ {ticker} のデータ取得成功！")

        except Exception as e:
            print(f"❌ {ticker} のデータ取得エラー: {e}")

    if all_data:
        df = pd.concat(all_data)
        csv_path = os.path.join(data_dir, "stock_data.csv")
        df.to_csv(csv_path)
        print(f"✅ データを {csv_path} に保存しました")
    else:
        print("⚠ 取得できたデータがありません。")

if __name__ == "__main__":
    fetch_and_save_data()
