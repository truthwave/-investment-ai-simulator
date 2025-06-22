import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime 

# .env ファイルを読み込む
load_dotenv()


class ExchangeAPI:
    def __init__(self, exchange="binance"):
        self.exchange = exchange
        self.api_key = "YOUR_API_KEY"
        self.api_secret = "YOUR_API_SECRET"
        self.base_url = "https://api.binance.com"

        # ログディレクトリ作成
        os.makedirs("logs", exist_ok=True)

    def log(self, message):
        """ログをファイルに記録"""
        with open("logs/trade_log.txt", "a") as f:
            f.write(f"{datetime.now()} - {message}\n")

    def get_market_price(self, symbol):
        """現在の市場価格を取得"""
        try:
            url = f"{self.base_url}/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url)
            data = response.json()
            if "price" in data:
                return float(data["price"])
            else:
                self.log(f"価格取得エラー: {data}")
                return None
        except requests.exceptions.RequestException as e:
            self.log(f"API通信エラー: {str(e)}")
            return None

    def place_order(self, symbol, side, amount, price=None):
        """注文を実行"""
        if not symbol or not isinstance(symbol, str):
            self.log("注文失敗: 無効なシンボルが渡されました")
            return {"error": "無効なシンボル"}

        if price is None:
            price = self.get_market_price(symbol)

        if price is None:
            self.log("注文失敗: 価格取得不可")
            return {"error": "価格が取得できません"}

        order_params = {
            "symbol": symbol,
            "side": side.upper(),
            "amount": amount,
            "price": price
        }

        # --- 送信データをログに記録 ---
        self.log(f"注文データ: {json.dumps(order_params, ensure_ascii=False)}")

        return order_params  # 実際のAPIリクエストはここで行う
