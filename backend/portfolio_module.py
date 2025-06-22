class Portfolio:
    def __init__(self):
        self.positions = {}  # 保有銘柄と購入価格を記録

    def buy(self, symbol, price):
        self.positions[symbol] = price
        print(f"[BUY] {symbol} @ {price}")

    def sell(self, symbol, price):
        if symbol in self.positions:
            del self.positions[symbol]
            print(f"[SELL] {symbol} @ {price}")
