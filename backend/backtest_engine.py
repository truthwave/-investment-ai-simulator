import pandas as pd
from strategy.strategy_selector import StrategySelector

class BacktestEngine:
    def __init__(
        self,
        initial_balance=1_000_000,
        entry_threshold=2.0,
        take_profit_atr_multiplier=2.0,
        stop_loss_atr_multiplier=1.0,
        lot_size=10000,
        use_compounding=False
    ):
        self.initial_balance = initial_balance
        self.balance = float(initial_balance)
        self.balance_history = [self.balance]
        self.position = None
        self.trade_log = []
        self.max_drawdown = 0.0
        self.peak_balance = self.balance
        self.returns = []

        self.lot_size = lot_size
        self.use_compounding = use_compounding

        self.strategy = StrategySelector(
            entry_threshold=entry_threshold,
            take_profit_atr_multiplier=take_profit_atr_multiplier,
            stop_loss_atr_multiplier=stop_loss_atr_multiplier
        )

    def run(self, df):
        df = self.strategy.calculate_indicators(df)

        for i in range(len(df)):
            row = df.iloc[i]

            # 決済判断
            if self.position:
                should_exit = self.strategy.should_exit(
                    self.position,
                    df.iloc[:i + 1]
                )

                if should_exit:
                    exit_price = row["close"]
                    entry_price = self.position["entry_price"]
                    side = self.position["side"]
                    position_lot = self.position["lot"]

                    if side == "buy":
                        pnl = (exit_price - entry_price) * position_lot
                    else:
                        pnl = (entry_price - exit_price) * position_lot

                    self.balance += pnl
                    self.returns.append(pnl)
                    self.trade_log.append(
                        f"{row['timestamp']} - {side.upper()} (TP/SL) @ {exit_price:.2f} (Lot: {position_lot})"
                    )
                    self.position = None

                    if self.balance > self.peak_balance:
                        self.peak_balance = self.balance
                    dd = 1 - self.balance / self.peak_balance
                    self.max_drawdown = max(self.max_drawdown, dd)

                    self.balance_history.append(self.balance)
                    continue

            # エントリー判断
            if not self.position:
                decision = self.strategy.should_trade(df.iloc[:i + 1])
                if decision:
                    lot = self.calculate_lot()
                    self.position = {
                        "side": decision,
                        "entry_price": row["close"],
                        "timestamp": row["timestamp"],
                        "lot": lot
                    }
                    self.trade_log.append(
                        f"{row['timestamp']} - {decision.upper()} @ {row['close']:.2f} (Lot: {lot})"
                    )

            self.balance_history.append(self.balance)

        return {
            "initial_balance": self.initial_balance,
            "final_balance": self.balance,
            "profit": self.balance - self.initial_balance,
            "balance_history": self.balance_history,
            "trades": self.trade_log,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.calculate_win_rate(),
            "sharpe_ratio": self.calculate_sharpe_ratio()
        }

    def calculate_lot(self):
        if self.use_compounding:
            return round(self.balance * 0.01 / 1000) * 1000  # 1%で1000円単位
        else:
            return self.lot_size

    def calculate_win_rate(self):
        wins = [r for r in self.returns if r > 0]
        total = len(self.returns)
        if total == 0:
            return 0.0
        return len(wins) / total * 100

    def calculate_sharpe_ratio(self):
        if len(self.returns) < 2:
            return 0.0
        series = pd.Series(self.returns)
        mean = series.mean()
        std = series.std()
        if std == 0:
            return 0.0
        return (mean / std) * (252 ** 0.5)
