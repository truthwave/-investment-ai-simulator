import logging
import pandas as pd
from ta.momentum import RSIIndicator
import requests
import os
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_fundamentals(symbol):
    """PER, ROE, EPS を取得する"""
    try:
        url = f"{FMP_BASE_URL}/ratios-ttm/{symbol}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if not data or not isinstance(data, list):
            raise ValueError("ファンダメンタルデータが取得できませんでした")

        first = data[0]
        return {
            "PE_ratio": float(first.get("peRatioTTM", 0)),
            "ROE": float(first.get("roeTTM", 0)),
            "EPS": float(first.get("epsTTM", 0))
        }
    except Exception as e:
        print(f"[ファンダメンタル取得失敗] {symbol}: {e}")
        return None



logger = logging.getLogger(__name__)

def calculate_indicators(df):
    # 例: 移動平均・MACD・RSIなどの追加
    df["ma_50"] = df["Close"].rolling(window=50).mean()
    df["ma_200"] = df["Close"].rolling(window=200).mean()

    # RSI
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # ✅ ボリンジャーバンド追加
    bb_middle = df["Close"].rolling(window=20).mean()
    bb_std = df["Close"].rolling(window=20).std()
    df["BB_bbm"] = bb_middle
    df["BB_bbu"] = bb_middle + (2 * bb_std)
    df["BB_bbl"] = bb_middle - (2 * bb_std)

    return df



def generate_signals(df, symbol="BTC/USDT"):
    df = df.copy()
    df["signal"] = None
    in_position = False
    buy_price = None

    take_profit_pct = 0.15   # 利確15%
    stop_loss_pct = 0.02     # 損切り2%
    trailing_stop_pct = 0.01 # トレーリング1%

    highest_price = None

    # 指標が必要な行に欠損がないことを保証
    df = df.dropna(subset=["ma_50", "ma_200", "RSI", "MACD", "MACD_signal"])

    for i in range(len(df)):
        row = df.iloc[i]
        current_price = row["Close"]

        # --- BUY条件 ---
        if not in_position:
            # パート３：エントリー条件の修正
            buy_condition = (
                row["ma_50"] > row["ma_200"] and          # 強気トレンド
                row["RSI"] > 55 and row["RSI"] < 65 and   # やや買われすぎ
                row["MACD"] > row["MACD_signal"]          # MACDゴールデンクロス
            )

            if buy_condition:
                df.iat[i, df.columns.get_loc("signal")] = "BUY"
                buy_price = current_price
                highest_price = current_price
                in_position = True

        # --- SELL条件 ---
        else:
            # 更新
            highest_price = max(highest_price, current_price)

            # 条件判定
            stop_loss = current_price <= buy_price * (1 - stop_loss_pct)
            take_profit = current_price >= buy_price * (1 + take_profit_pct)
            trailing_stop = current_price <= highest_price * (1 - trailing_stop_pct)
            trend_reversal = row["ma_50"] < row["ma_200"] or row["RSI"] > 70

            if stop_loss or take_profit or trailing_stop or trend_reversal:
                df.iat[i, df.columns.get_loc("signal")] = "SELL"
                in_position = False
                buy_price = None
                highest_price = None

    return df




def is_buffett_candidate(fundamentals):
    """バフェット基準：割安・健全な財務・収益性"""
    if not fundamentals:
        return False

    return (
        fundamentals["PE_ratio"] < 15 and
        fundamentals["ROE"] > 10 and
        fundamentals["EPS"] > 0
    )

