import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QLineEdit
from backend.trading_manager import TradingManager

class TradingGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = TradingManager(mode="virtual")  # デフォルトは仮想取引

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("取引モード:")
        layout.addWidget(self.label)

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
        result = self.manager.place_order("buy", amount)
        self.status_label.setText(result)

    def place_sell_order(self):
        amount = float(self.amount_input.text())
        result = self.manager.place_order("sell", amount)
        self.status_label.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TradingGUI()
    sys.exit(app.exec_())
