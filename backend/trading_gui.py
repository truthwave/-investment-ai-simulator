import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget
from backend.trading_manager import TradingManager
import threading
import time

class TradingGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = TradingManager(mode="virtual")
        self.initUI()

        # 価格更新スレッド
        self.running = True
        self.price_thread = threading.Thread(target=self.update_price_loop)
        self.price_thread.start()

    def initUI(self):
        layout = QVBoxLayout()

        self.price_label = QLabel("現在のBTC価格: 取得中...")
        layout.addWidget(self.price_label)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["virtual", "api"])
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        layout.addWidget(self.mode_selector)

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("数量 (BTC)")
        layout.addWidget(self.amount_input)

        self.buy_button = QPushButton("買い注文")
        self.buy_button.clicked.connect(self.place_buy_order)
        layout.addWidget(self.buy_button)

        self.sell_button = QPushButton("売り注文")
        self.sell_button.clicked.connect(self.place_sell_order)
        layout.addWidget(self.sell_button)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        self.load_trade_history()

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setWindowTitle("仮想取引 & API取引")
        self.show()

    def change_mode(self, mode):
        self.manager.mode = mode
        self.status_label.setText(f"モード変更: {mode}")

    def place_buy_order(self):
        amount = float(self.amount_input.text())
        trade = self.manager.place_order("buy", amount)
        self.status_label.setText(f"購入成功: {trade['amount']} BTC @ {trade['price']} USD")
        self.load_trade_history()

    def place_sell_order(self):
        amount = float(self.amount_input.text())
        trade = self.manager.place_order("sell", amount)
        self.status_label.setText(f"売却成功: {trade['amount']} BTC @ {trade['price']} USD")
        self.load_trade_history()

    def load_trade_history(self):
        self.history_list.clear()
        for trade in self.manager.trade_history[-5:]:  # 最新5件を表示
            self.history_list.addItem(f"{trade['timestamp']} | {trade['type']} {trade['amount']} BTC @ {trade['price']} USD")

    def update_price_loop(self):
        while self.running:
            if self.manager.mode == "virtual":
                self.manager.exchange.update_price()
                price = self.manager.exchange.price
            else:
                price = self.manager.exchange.get_real_time_price()

            self.price_label.setText(f"現在のBTC価格: {price} USD")
            time.sleep(2)

    def closeEvent(self, event):
        self.running = False
        self.price_thread.join()
        event.accept()
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget
from PyQt5.QtCore import QTimer
from trading_manager import TradingManager

class TradingGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = TradingManager(mode="virtual")
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_price_display)
        self.timer.start(1000)  # 1秒ごとに価格を更新

    def initUI(self):
        layout = QVBoxLayout()

        self.price_label = QLabel("現在のBTC価格: 取得中...")
        layout.addWidget(self.price_label)

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("数量 (BTC)")
        layout.addWidget(self.amount_input)

        self.buy_button = QPushButton("買い注文")
        self.buy_button.clicked.connect(self.place_buy_order)
        layout.addWidget(self.buy_button)

        self.sell_button = QPushButton("売り注文")
        self.sell_button.clicked.connect(self.place_sell_order)
        layout.addWidget(self.sell_button)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        self.setLayout(layout)
        self.setWindowTitle("仮想取引システム")
        self.show()

    def update_price_display(self):
        """リアルタイムで価格を更新"""
        price = self.manager.get_price()
        self.price_label.setText(f"現在のBTC価格: {price} USD")

    def place_buy_order(self):
        amount = float(self.amount_input.text())
        price = self.manager.place_order("buy", amount)
        self.history_list.addItem(f"買い: {amount} BTC @ {price} USD")

    def place_sell_order(self):
        amount = float(self.amount_input.text())
        price = self.manager.place_order("sell", amount)
        self.history_list.addItem(f"売り: {amount} BTC @ {price} USD")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TradingGUI()
    sys.exit(app.exec_())
import sys
import json
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget
from PyQt5.QtCore import QTimer


class TradingGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = TradingManager(mode="virtual")  # デフォルトは仮想取引

        self.initUI()
        self.update_price()  # 初回価格取得
        self.load_trade_history()

        # タイマーで価格を自動更新（1秒ごと）
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_price)
        self.timer.start(1000)

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("取引モード:")
        layout.addWidget(self.label)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["virtual", "api"])
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        layout.addWidget(self.mode_selector)

        self.price_label = QLabel("現在の価格: -")
        layout.addWidget(self.price_label)

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("数量 (BTC)")
        layout.addWidget(self.amount_input)

        self.buy_button = QPushButton("買い注文")
        self.buy_button.clicked.connect(self.place_buy_order)
        layout.addWidget(self.buy_button)

        self.sell_button = QPushButton("売り注文")
        self.sell_button.clicked.connect(self.place_sell_order)
        layout.addWidget(self.sell_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.trade_history_list = QListWidget()
        layout.addWidget(self.trade_history_list)

        self.setLayout(layout)
        self.setWindowTitle("仮想取引 & API取引")
        self.show()

    def change_mode(self, mode):
        self.manager.mode = mode
        self.status_label.setText(f"モード変更: {mode}")

    def update_price(self):
        """現在のBTC価格を更新"""
        price = self.manager.get_price()
        self.price_label.setText(f"現在の価格: {price:.2f} USD")

    def place_buy_order(self):
        self.execute_trade("buy")

    def place_sell_order(self):
        self.execute_trade("sell")

    def execute_trade(self, order_type):
        amount = float(self.amount_input.text())
        result = self.manager.place_order(order_type, amount)
        self.status_label.setText(f"{order_type.upper()} 注文成功: {result:.2f} USD")
        self.load_trade_history()  # 取引履歴を更新

    def load_trade_history(self):
        """取引履歴をロードしてGUIに表示"""
        self.trade_history_list.clear()
        try:
            with open("trade_history.json", "r") as f:
                trade_history = json.load(f)
                for trade in trade_history:
                    text = f"{trade['timestamp']} - {trade['type'].upper()} {trade['amount']} BTC @ {trade['price']} USD"
                    self.trade_history_list.addItem(text)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TradingGUI()
    sys.exit(app.exec_())
