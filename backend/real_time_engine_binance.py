import requests
import pandas as pd
import datetime
from strategy.strategy_selector import StrategySelector
from notifier import send_email

# 対象シンボル（Binance形式）
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
LOOKBACK = 50  # 過去50本で判断

# Binance Kline API URL
def get_binance_ohlcv(symbol=SYMBOL, interval=INTERVAL, limit=LOOKBACK):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    raw = res.json()
    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "high", "low", "close",
        "volume", "close_time", "quote_asset_volume",
        "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df[["timestamp", "open", "high", "low", "close", "volume"]]

# メイン処理
def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏰ {now} - 実運用シグナル判定開始（Binance BTCUSDT）")

    try:
        df = get_binance_ohlcv()

        selector = StrategySelector()
        df = selector.calculate_indicators(df)

        signal = selector.should_trade(df)
        if signal:
            latest = df.iloc[-1]
            message = (
                f"[{latest['timestamp']}] BTCUSDT にエントリーシグナル\n"
                f"方向: {signal.upper()}\n"
                f"価格: ${latest['close']:.2f}"
            )
            send_email("📈 Binance シグナル検出", message)
        else:
            print("📭 シグナルなし")

    except Exception as e:
        print(f"📛 エラー: {e}")

if __name__ == "__main__":
    main()
    with open("signal_log.txt", "a", encoding="utf-8") as log:
            log.write(f"[{datetime.datetime.now()}] ✅ タスク実行完了\n")