import pandas as pd

class Backtester:
    def __init__(self, data):
        self.data = data.copy()
        self.initial_cash = 1000000  # 初期資金: 100万円
        self.cash = self.initial_cash
        self.position = 0
        self.buy_price = 0
        self.trades = []

    def run(self):
        for i in range(len(self.data)):
            row = self.data.iloc[i]

            # BUY 条件
            if row["signal"] == "BUY" and self.position == 0:
                self.buy_price = row["Close"]
                self.position = self.cash / self.buy_price
                self.cash = 0
                self.trades.append({"date": row.name, "action": "BUY", "price": self.buy_price})

            # SELL 条件
            elif row["signal"] == "SELL" and self.position > 0:
                sell_price = row["Close"]
                self.cash = self.position * sell_price
                self.position = 0
                self.trades.append({"date": row.name, "action": "SELL", "price": sell_price})

        # 最終評価
        final_value = self.cash + self.position * self.data.iloc[-1]["Close"]
        return {
            "initial_cash": self.initial_cash,
            "final_value": final_value,
            "profit": final_value - self.initial_cash,
            "trades": self.trades
        }
