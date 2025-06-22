# strategy/box_strategy.py

import pandas as pd
import numpy as np

class BoxStrategy:
    def __init__(self, support_window=20, resistance_window=20):
        self.support_window = support_window
        self.resistance_window = resistance_window

    def calculate_indicators(self, df):
        df["support"] = df["low"].rolling(window=self.support_window).min()
        df["resistance"] = df["high"].rolling(window=self.resistance_window).max()

        df["prev_close"] = df["close"].shift(1)
        df["tr1"] = df["high"] - df["low"]
        df["tr2"] = (df["high"] - df["prev_close"]).abs()
        df["tr3"] = (df["low"] - df["prev_close"]).abs()
        df["tr"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
        df["ATR"] = df["tr"].rolling(window=14).mean()

        return df

    def should_trade(self, df):
        if len(df) < 35:
            return None

        latest = df.iloc[-1]

        if (
            latest["close"] <= latest["support"] * 1.01
        ):
            return "buy"
        elif (
            latest["close"] >= latest["resistance"] * 0.99
        ):
            return "sell"
        return None

    def should_exit(self, position, df):
        latest = df.iloc[-1]
        atr = latest["ATR"]

        if position["side"] == "buy":
            if latest["close"] >= position["entry_price"] + 1.2 * atr:
                return True
            elif latest["close"] <= position["entry_price"] - 0.8 * atr:
                return True
        elif position["side"] == "sell":
            if latest["close"] <= position["entry_price"] - 1.2 * atr:
                return True
            elif latest["close"] >= position["entry_price"] + 0.8 * atr:
                return True
        return False
