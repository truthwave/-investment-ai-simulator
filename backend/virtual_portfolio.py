# ==========================
# virtual_portfolio.py
# 仮想取引管理モジュール（取引履歴記録版）
# ==========================

import pandas as pd
from notifier import send_trade_signal
from datetime import datetime
import os

# 履歴保存ファイル
HISTORY_FILE = 'trade_history.csv'

class VirtualPortfolio:
    def __init__(self, initial_cash=10000, fee_rate=0.001, profit_take=0.30, stop_loss=0.15):
        self.cash = initial_cash
        self.position = 0
        self.avg_entry_price = 0
        self.fee_rate = fee_rate
        self.profit_take = profit_take
        self.stop_loss = stop_loss

    def can_buy(self, price):
        return self.cash > price

    def _record_trade(self, symbol, trade_type, price, quantity, profit=None):
        """
        取引履歴をtrade_history.csvに記録する
        """
        now = datetime.now()
        trade = {
            'date': now.strftime("%Y-%m-%d"),
            'time': now.strftime("%H:%M:%S"),
            'symbol': symbol,
            'type': trade_type,
            'price': price,
            'quantity': quantity,
            'profit': profit if profit is not None else ''
        }
        
        df_trade = pd.DataFrame([trade])

        if os.path.exists(HISTORY_FILE):
            df_trade.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
        else:
            df_trade.to_csv(HISTORY_FILE, mode='w', header=True, index=False)

    def buy(self, price):
        if self.can_buy(price):
            quantity = self.cash * (1 - self.fee_rate) / price
            self.position = quantity
            self.avg_entry_price = price
            self.cash = 0

            send_trade_signal(
                subject="【エントリーシグナル】",
                body=(
                    f"エントリー条件達成！\n"
                    f"買付価格：{price:.2f}円\n"
                    f"ポジション数量：{self.position:.4f}\n"
                    f"仮想資金残高：{self.cash:.2f}円"
                )
            )

            # 取引記録
            self._record_trade(
                symbol="仮想取引",
                trade_type="entry",
                price=price,
                quantity=self.position
            )

    def sell(self, price, reason):
        if self.position > 0:
            proceeds = self.position * price * (1 - self.fee_rate)
            profit = proceeds - (self.position * self.avg_entry_price)

            self.cash = proceeds
            send_trade_signal(
                subject="【イグジットシグナル】",
                body=(
                    f"売却理由：{reason}\n"
                    f"売却価格：{price:.2f}円\n"
                    f"受取資金：{self.cash:.2f}円\n"
                    f"仮想資金残高：{self.cash:.2f}円"
                )
            )

            # 取引記録
            self._record_trade(
                symbol="仮想取引",
                trade_type="exit",
                price=price,
                quantity=self.position,
                profit=profit
            )

            self.position = 0
            self.avg_entry_price = 0

    def check_exit_conditions(self, current_price):
        if self.position == 0:
            return False

        profit_ratio = (current_price - self.avg_entry_price) / self.avg_entry_price

        if profit_ratio >= self.profit_take:
            self.sell(current_price, reason=f"利益確定（+{self.profit_take * 100:.0f}%超）")
            return True

        if profit_ratio <= -self.stop_loss:
            self.sell(current_price, reason=f"損切り（-{self.stop_loss * 100:.0f}%超）")
            return True

        return False

    def force_sell(self, price):
        if self.position > 0:
            self.sell(price, reason="デッドクロス発生による売却")
