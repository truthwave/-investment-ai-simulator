import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TradeHistory:
    """取引履歴をCSVファイルに記録および取得するクラス"""

    def __init__(self, filename: str = "trade_history.csv"):
        self.filename = filename
        self.fields = ["date", "ticker", "action", "price", "quantity", "profit_loss"]

    def log_trade(self, ticker: str, action: str, price: float, quantity: int, profit_loss: Optional[float] = None) -> None:
        """取引履歴をCSVファイルに記録する

        Args:
            ticker (str): ティッカーシンボル
            action (str): アクション（buy または sell）
            price (float): 価格
            quantity (int): 数量
            profit_loss (Optional[float], optional): 損益.None の場合は損益を記録しません。 Defaults to None.
        """
        file_exists = os.path.exists(self.filename)
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(self.fields)  # ヘッダーを書き込む
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ticker, action, price, quantity, profit_loss])

    def get_trade_history(self) -> List[Dict[str, str]]:
        """保存された取引履歴を取得する

        Returns:
            List[Dict[str, str]]: 取引履歴のリスト
        """
        if not os.path.exists(self.filename):
            return []  # ファイルが存在しない場合は空のリストを返す
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            logging.error(f"Error reading trade history: {e}")
            return []