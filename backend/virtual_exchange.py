import csv
from datetime import datetime

# 仮想取引所クラス
# virtual_exchange.py

class VirtualExchange:
    def __init__(self):
        self.balance = {
            "BTC": 0.0,
            "JPY": 1000000.0,
            "USDT": 1000000.0 
        }
        self.price = {
            "BTC/JPY": 7000000.0,
            "USDT": 1000000.0 
        }
        self.avg_buy_price = {}
        self.realized_pnl_log = []  # ← ここでログを初期化
        self.trade_history = []

    def get_price(self, base_currency, quote_currency):
        return self.price.get(f"{base_currency}/{quote_currency}", 0.0)

    def buy(self, base_currency, quote_currency, amount):
        price = self.get_price(base_currency, quote_currency)
        cost = price * amount
        if self.balance.get(quote_currency, 0.0) >= cost:
            self.balance[quote_currency] -= cost
            self.balance[base_currency] += amount
            self.avg_buy_price[base_currency] = price
            self.trade_history.append({
            "timestamp": datetime.now().isoformat(),
            "side": "buy",
            "base_currency": base_currency,
            "quote_currency": quote_currency,
            "amount": amount,
            "price": price
        })
            return {"status": "success", "price": price}
        else:
            return {"status": "error", "message": "Insufficient balance"}
        
    def sell(self, base_currency, quote_currency, amount):
        price = self.get_price(base_currency, quote_currency)
        proceeds = price * amount
        if self.balance.get(base_currency, 0.0) >= amount:
            self.balance[base_currency] -= amount
            self.balance[quote_currency] += proceeds

            # 実現損益の計算と記録
            avg_price = self.avg_buy_price.get(base_currency, price)
            pnl = (price - avg_price) * amount

            # 実現損益ログに記録
            self.realized_pnl_log.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "currency": base_currency,
                "amount": amount,
                "sell_price": price,
                "avg_price": avg_price,
                "realized_pnl": pnl
            })

            return {"status": "success", "price": price, "realized_pnl": pnl}
        else:
            return {"status": "error", "message": "Insufficient balance"}

    def get_realized_pnl_log(self):
        return self.realized_pnl_log


    def get_trade_history(self):
        return self.trade_history
