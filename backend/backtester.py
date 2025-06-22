import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, data):
        self.data = data.copy()
        self.initial_cash = 1000000
        self.cash = self.initial_cash
        self.position = 0
        self.buy_price = 0
        self.trades = []
        self.trade_log = []

    def run(self):
        portfolio_values = []

        for index, row in self.data.iterrows():
            price = row["Close"]
            signal = row.get("signal", None)

            if signal == "BUY" and self.position == 0:
                self.position = 0.01
                self.buy_price = price
                self.cash -= self.position * price
                self.trade_log.append({
                    "timestamp": index,
                    "symbol": "BTCUSDT",
                    "side": "buy",
                    "entry_price": price,
                    "exit_price": None,
                    "amount": self.position,
                    "pnl": None
                })

            elif signal == "SELL" and self.position > 0:
                self.cash += self.position * price
                pnl = (price - self.buy_price) * self.position
                self.trade_log[-1]["exit_price"] = price
                self.trade_log[-1]["pnl"] = pnl
                self.position = 0
                self.buy_price = 0

            portfolio_value = self.cash + self.position * price
            portfolio_values.append(portfolio_value)

        self.data["portfolio_value"] = portfolio_values

        return {
            "initial_cash": self.initial_cash,
            "final_value": self.data["portfolio_value"].iloc[-1],
            "pnl": self.data["portfolio_value"].iloc[-1] - self.initial_cash,
            "max_drawdown": self.calculate_max_drawdown(),
            "trade_log": self.trade_log,
            "win_rate": self.calculate_win_rate(),
            "sharpe_ratio": self.calculate_sharpe_ratio()
        }

    def calculate_max_drawdown(self):
        equity_curve = self.data["portfolio_value"]
        peak = equity_curve.expanding(min_periods=1).max()
        drawdown = (peak - equity_curve) / peak
        return drawdown.max()

    def calculate_win_rate(self):
        wins = 0
        total = 0
        for trade in self.trade_log:
            if "pnl" in trade and trade["pnl"] is not None:
                total += 1
                if trade["pnl"] > 0:
                    wins += 1
        return wins / total if total > 0 else 0

    def calculate_sharpe_ratio(self):
        returns = self.data["portfolio_value"].pct_change().dropna()
        if returns.std() == 0 or returns.empty:
            return 0.0
        sharpe = returns.mean() / returns.std() * np.sqrt(252)
        return sharpe
