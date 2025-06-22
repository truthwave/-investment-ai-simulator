import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker, period="1y", interval="1d"):
    """
    Yahoo Finance API を使用して株価データを取得する関数

    :param ticker: 銘柄コード (例: "AAPL")
    :param period: 取得期間 (例: "1mo", "3mo", "1y", "5y")
    :param interval: 取得間隔 (例: "1d", "1wk", "1mo")
    :return: データフレーム
    """
    try:
        stock_data = yf.download(ticker, period=period, interval=interval)
        if stock_data.empty:
            print(f"⚠️ {ticker} のデータが取得できませんでした。")
            return None
        print(f"✅ {ticker} のデータを取得しました！")
        return stock_data
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return None

if __name__ == "__main__":
    ticker_symbol = "AAPL"  # Appleの株価データを取得
    data = get_stock_data(ticker_symbol)

    if data is not None:
        print("\n📊 データの統計情報:")
        print(data.describe())  # 統計情報を表示

        # 📈 株価の推移をプロット
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data["Close"], label="終値", color="blue")
        plt.xlabel("日付")
        plt.ylabel("株価 ($)")
        plt.title(f"{ticker_symbol} 株価推移")
        plt.legend()
        plt.grid()

        # 画像として保存
        plt.savefig("stock_price_plot.png")
        print("✅ グラフを 'stock_price_plot.png' に保存しました！")

        # グラフを表示
        plt.show()

# get_stock_data.py
import logging
import pandas as pd

def get_price_data(symbol):
    try:
        df = yf.download(symbol, period="6mo", interval="1d", progress=False)
        if df.empty:
            raise ValueError("取得結果が空です")
        if 'Close' not in df.columns:
            raise ValueError("'Close' 列がありません")

        df = df[['Close']].copy()  # 必要な列だけにして明確化
        df.dropna(inplace=True)
        return df

    except Exception as e:
        print(f"[データ取得エラー] {symbol}: {e}")
        return pd.DataFrame()  # 空DataFrameで返す（呼び出し側で処理）

logger = logging.getLogger(__name__)

def get_price_data(symbol):
    try:
        df = yf.download(symbol, period="6mo", interval="1d", progress=False)
        if df.empty:
            logger.error(f"[データ取得エラー] {symbol}: データが空です")
            return pd.DataFrame()

        if 'Close' not in df.columns:
            logger.error(f"[データ取得エラー] {symbol}: 'Close'列がありません")
            return pd.DataFrame()

        df = df[['Close']].copy()
        df.dropna(inplace=True)
        return df

    except Exception as e:
        logger.exception(f"[データ取得エラー] {symbol}: {e}")
        return pd.DataFrame()
