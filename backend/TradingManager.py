from api_client import ExchangeAPI
from backend.virtual_exchange import VirtualExchange

# パート１：取引マネージャクラス定義
# trading_manager.py

class TradingManager:
    def __init__(self, mode="virtual", exchange=None):
        self.mode = mode
        self.exchange = exchange
        print(f"取引モード: {self.mode}")

        if self.mode == "api":
            self.initialize_api(exchange)
        else:
            self.initialize_virtual()

    def initialize_virtual(self):
        print("仮想取引モードを初期化しました")

    def initialize_api(self, exchange):
        print(f"{exchange} API取引モードを初期化しました")

    def place_order(self, side, amount):
        print(f"{self.mode}モードで注文：{side} {amount}")
