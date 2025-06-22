import pandas as pd
import numpy as np

class TradeStrategy:
    def __init__(self):
        pass

    # パート1：インジケーターの計算
    def calculate_indicators(self, df):
        df = df.copy()
        
        # ボリンジャーバンド
        df["ma"] = df["close"].rolling(window=20).mean()
        df["std"] = df["close"].rolling(window=20).std()
        df["bb_upper"] = df["ma"] + 2 * df["std"]
        df["bb_lower"] = df["ma"] - 2 * df["std"]

        # ATR（Average True Range）
        df["prev_close"] = df["close"].shift(1)
        df["tr1"] = df["high"] - df["low"]
        df["tr2"] = (df["high"] - df["prev_close"]).abs()
        df["tr3"] = (df["low"] - df["prev_close"]).abs()
        df["tr"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
        df["ATR"] = df["tr"].rolling(window=14).mean()

        # 出来高移動平均
        df["volume_ma"] = df["volume"].rolling(window=20).mean()

        # ADX（Average Directional Index）
        high = df["high"]
        low = df["low"]
        close = df["close"]
        plus_dm = high.diff()
        minus_dm = -low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0

        tr = df["tr"]
        atr = df["ATR"]
        plus_di = 100 * (plus_dm.rolling(window=14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=14).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(window=14).mean()
        df["adx"] = adx

        return df

    # パート2：エントリー条件の判断
    def should_trade(self, df):
        if len(df) < 35:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        atr_mean = df["ATR"].rolling(window=20).mean().iloc[-1]
        volume_mean = df["volume_ma"].iloc[-1]

        if (
            latest["ma"] > prev["ma"] and
            latest["ATR"] > atr_mean and
            latest["volume"] > volume_mean and
            latest["adx"] > 30 and
            latest["adx"] > prev["adx"]
        ):
            return "buy"

        return None

    # パート3：決済条件の判断
    def should_exit(self, position, df, take_profit_atr_multiplier, stop_loss_atr_multiplier):
        if len(df) < 2:
            return False

        latest = df.iloc[-1]
        atr = latest["ATR"]

        if position["side"] == "buy":
            if latest["close"] >= position["entry_price"] + take_profit_atr_multiplier * atr:
                return True
            if latest["close"] <= position["entry_price"] - stop_loss_atr_multiplier * atr:
                return True

        return False
