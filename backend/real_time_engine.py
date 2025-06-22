import os
import yfinance as yf
from dotenv import load_dotenv
from strategy.strategy_selector import StrategySelector
from notifier import send_email
import datetime

# .env読み込み
load_dotenv()

SYMBOL = os.getenv("TARGET_SYMBOL", "^N225")  # デフォルトは日経平均
INTERVAL = os.getenv("INTERVAL", "1m")
LOOKBACK = int(os.getenv("LOOKBACK", 50))     # 過去n本のデータで判断
EMAIL_TO = os.getenv("NOTIFY_TO_ADDRESS")

def get_latest_data(symbol, lookback=50):
    df = yf.download(tickers=symbol, period="7d", interval="1m", progress=False)
    if df.empty:
        raise ValueError(f"価格データ取得失敗: {symbol}")
    df = df.reset_index()
    df.columns = [c.lower() for c in df.columns]
    df.rename(columns={"datetime": "timestamp"}, inplace=True)
    return df.tail(lookback)

def main():
    print(f"⏰ {datetime.datetime.now()} - 実運用シグナル判定開始")

    try:
        df = get_latest_data(SYMBOL, lookback=LOOKBACK)

        selector = StrategySelector()
        df = selector.calculate_indicators(df)

        signal = selector.should_trade(df)
        if signal:
            price = df.iloc[-1]["close"]
            timestamp = df.iloc[-1]["timestamp"]
            message = f"[{timestamp}] {SYMBOL} にエントリーシグナル: {signal.upper()} @ {price:.2f}"
            send_email(f"📈 シグナル検出: {signal.upper()}", message)
        else:
            print("📭 シグナルなし")
    except Exception as e:
        print(f"📛 エラー: {e}")

if __name__ == "__main__":
    main()
