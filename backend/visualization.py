import matplotlib.pyplot as plt
import numpy as np
import os
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ProfitVisualization:
    def __init__(self, image_path: str = "backend/profit_graph.png"):
        self.image_path = image_path  # 画像保存パス

    def generate_mock_profit_data(self, days: int = 30, initial_balance: float = 100000, daily_return_mean: float = 1.01, daily_return_scale: float = 0.02) -> list:
        """
        仮想データを生成（指定した日数分の損益）
        - 指定した日利で増加するパターン
        - 価格変動をランダムに追加
        """
        np.random.seed(42)
        daily_returns = np.random.normal(loc=daily_return_mean, scale=daily_return_scale, size=days)
        balance = [initial_balance]

        for r in daily_returns:
            balance.append(balance[-1] * r)

        return balance

    def save_profit_graph(self, days: int = 30, initial_balance: float = 100000, daily_return_mean: float = 1.01, daily_return_scale: float = 0.02,
                          title: str = "仮想データによる損益シミュレーション", xlabel: str = "日数", ylabel: str = "資産額（円）", label: str = "損益") -> str:
        """
        損益のグラフを画像として保存
        """
        profit_data = self.generate_mock_profit_data(days, initial_balance, daily_return_mean, daily_return_scale)
        days_range = np.arange(len(profit_data))

        plt.figure(figsize=(10, 5))
        plt.plot(days_range, profit_data, marker="o", linestyle="-", color="b", label=label)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.grid()

        # 画像を保存
        try:
            plt.savefig(self.image_path)
            plt.close()
            return self.image_path
        except Exception as e:
            logging.error(f"Error saving profit graph: {e}")
            return None
        import matplotlib.pyplot as plt
import time

class TradeVisualizer:
    def __init__(self):
        self.prices = []
        self.profits = []
        self.trades = []
        self.fig, self.ax1 = plt.subplots()

    def update_chart(self, current_price, total_profit, trade_action=None):
        """グラフをリアルタイム更新"""
        self.prices.append(current_price)
        self.profits.append(total_profit)

        self.ax1.clear()
        self.ax1.plot(self.prices, label="Price", color="blue")
        self.ax1.set_ylabel("Price", color="blue")

        self.ax2 = self.ax1.twinx()
        self.ax2.plot(self.profits, label="Profit", color="green")
        self.ax2.set_ylabel("Profit", color="green")

        if trade_action:
            self.trades.append(len(self.prices))
            self.ax1.scatter(self.trades, [self.prices[i] for i in self.trades], c="red", label="Trades")

        plt.pause(0.1)

    def show_chart(self):
        """グラフを表示"""
        plt.show()
