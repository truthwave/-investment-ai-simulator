# range_strategy.py

import pandas as pd
import numpy as np

class RangeStrategy:
    def __init__(self, entry_threshold=2.0):
        self.entry_threshold = entry_threshold

    # パート1：インジケーターの計算
    def calculate_indicators(self, df):
        df = df.copy()
        df["ma"] = df["close"].rolling(window=20).mean()
        df["std"] = df["close"].rolling(window=20).std()
        df["bb_upper"] = df["ma"] + self.entry_threshold * df["std"]
        df["bb_lower"] = df["ma"] - self.entry_threshold * df["std"]

        df["prev_close"] = df["close"].shift(1)
        df["tr1"] = df["high"] - df["low"]
        df["tr2"] = (df["high"] - df["prev_close"]).abs()
        df["tr3"] = (df["low"] - df["prev_close"]).abs()
        df["tr"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
        df["ATR"] = df["tr"].rolling(window=14).mean()

        df["volume_ma"] = df["volume"].rolling(window=20).mean()

        # ADX計算
        df["plus_dm"] = np.where((df["high"] - df["high"].shift(1)) > (df["low"].shift(1) - df["low"]),
                                 df["high"] - df["high"].shift(1), 0)
        df["plus_dm"] = np.where(df["plus_dm"] < 0, 0, df["plus_dm"])
        df["minus_dm"] = np.where((df["low"].shift(1) - df["low"]) > (df["high"] - df["high"].shift(1)),
                                  df["low"].shift(1) - df["low"], 0)
        df["minus_dm"] = np.where(df["minus_dm"] < 0, 0, df["minus_dm"])

        df["atr_14"] = df["tr"].rolling(window=14).mean()
        df["pdi"] = 100 * (df["plus_dm"].rolling(14).sum() / df["atr_14"])
        df["mdi"] = 100 * (df["minus_dm"].rolling(14).sum() / df["atr_14"])
        df["dx"] = 100 * (np.abs(df["pdi"] - df["mdi"]) / (df["pdi"] + df["mdi"]))
        df["adx"] = df["dx"].rolling(14).mean()

        return df

    # パート2：逆張りエントリー判断（ADX < 20がポイント）
    def should_trade(self, df):
        if len(df) < 35:
            return None

        latest = df.iloc[-1]
        atr_mean = df["ATR"].rolling(window=20).mean().iloc[-1]
        volume_mean = df["volume_ma"].iloc[-1]

        if (
            latest["close"] < latest["bb_lower"] and
            latest["adx"] < 20 and
            latest["ATR"] < atr_mean and
            latest["volume"] > volume_mean
        ):
            return "buy"  # 下限での反発狙い

        elif (
            latest["close"] > latest["bb_upper"] and
            latest["adx"] < 20 and
            latest["ATR"] < atr_mean and
            latest["volume"] > volume_mean
        ):
            return "sell"  # 上限での反落狙い

        return None

    # パート3：決済条件（TP/SL）
    def should_exit(self, position, df, take_profit_atr_multiplier, stop_loss_atr_multiplier):
        if len(df) < 2:
            return False

        latest = df.iloc[-1]
        atr = latest["ATR"]
        entry_price = position["entry_price"]

        if position["side"] == "buy":
            if latest["close"] >= entry_price + take_profit_atr_multiplier * atr:
                return True
            elif latest["close"] <= entry_price - stop_loss_atr_multiplier * atr:
                return True

        elif position["side"] == "sell":
            if latest["close"] <= entry_price - take_profit_atr_multiplier * atr:
                return True
            elif latest["close"] >= entry_price + stop_loss_atr_multiplier * atr:
                return True

        return False
