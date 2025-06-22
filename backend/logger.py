# logger.py

import pandas as pd

class TradeLogger:
    def __init__(self):
        self.logs = []

    def log_order(self, order):
        self.logs.append({
            "type": "entry",
            "symbol": order["symbol"],
            "side": order["side"],
            "price": order["entry_price"],
            "amount": order["amount"]
        })

    def log_close(self, position, reason, pnl):
        self.logs.append({
            "type": "exit",
            "symbol": position["symbol"],
            "side": position["side"],
            "exit_price": position["take_profit"] if reason == "利確" else position["stop_loss"],
            "reason": reason,
            "pnl": pnl
        })

    def summarize(self, exchange):
        df = pd.DataFrame(self.logs)
        print("最終残高:", exchange.get_balance())
        print("取引ログ:")
        print(df)

        df.to_csv("trade_log.csv", index=False)
# logger.py

from datetime import datetime
import os

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"trade_log_{datetime.now().date()}.txt")

    def log(self, message):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {message}\n")

    def log_trade(self, order):
        self.log(f"エントリー: {order}")

    def log_close(self, position, reason, result):
        self.log(f"決済（{reason}）: {position}, 損益: {result:.2f}")
