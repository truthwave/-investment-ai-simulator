# trading_manager.py

import pandas as pd
from backend.strategy import TradeStrategy
from backend.virtual_exchange import VirtualExchange
from backend.logger import Logger
from backend.ml_model import MLTradeModel
from backend.api_client import ExchangeAPI
import random
import asyncio
from backend.config_loader import load_config
from  backend.multi_timeframe_loader import load_candles, merge_timeframes
import logging
from datetime import datetime

# パート：TradingManager クラス
class TradingManager:
    def __init__(self, exchange, base_currency, quote_currency, mode="virtual"):
        self.exchange = exchange
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.mode = mode

        # ✅ logger の初期化（追加）
        self.logger = logging.getLogger(__name__)
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def place_order(self, side, amount):
        if side == "buy":
            result = self.exchange.buy(self.base_currency, self.quote_currency, amount)
        elif side == "sell":
            result = self.exchange.sell(self.base_currency, self.quote_currency, amount)
        else:
            raise ValueError("side must be 'buy' or 'sell'")
        
        self.logger.info(f"{side} オーダーを発行しました: {result}")
        return result


    # 👇 これを追加
    def check_signal(self):
        # 本来はAIやテクニカル指標を使いますが、まずは仮実装としてランダムにします
        return random.choice(["buy", "sell", None])


        if self.mode == "api":
            self.exchange = ExchangeAPI(
                api_key=config["api_key"],
                api_secret=config["api_secret"]
            )
        else:
            self.exchange = VirtualExchange()

        
        self.max_trades_per_day = 10

    # 追加：トレードをスタートする
    def start_trading(self):
        self.trading = True
        asyncio.create_task(self.run_trading_loop())
        print("✅ トレードを開始しました")

    # 追加：トレードを止める
    def stop_trading(self):
        self.trading = False
        print("🛑 トレードを停止しました")

    # 新規追加：非同期トレード監視ループ
    async def run_trading_loop(self):
        print("🔁 トレード監視ループを開始しました")
        while self.trading:
            print("🔍 シグナルを確認中...")

            signal = self.strategy.get_trade_signal()  # ※戦略クラスに合わせて調整
            print(f"📊 シグナル: {signal}")

            if signal == "buy":
                print("🟢 買いシグナル検出 → 注文")
                self.place_order("buy", 0.1)
            elif signal == "sell":
                print("🔴 売りシグナル検出 → 注文")
                self.place_order("sell", 0.1)
            else:
                print("⚪ シグナルなし → 待機中")

            await asyncio.sleep(10)  # 10秒おきに監視

    # パートX：注文実行機能
    # 注文を発行する
    
    def calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def run_strategy(self):
        # データ取得
        df_5m = load_candles("5m")
        df_1h = load_candles("1h")
        df = merge_timeframes(df_5m, df_1h)

        # テクニカル指標の計算
        df["ma"] = df["close"].rolling(window=14).mean()
        df["rsi"] = self.calculate_rsi(df["close"])
        df["ema12"] = df["close"].ewm(span=12, adjust=False).mean()
        df["ema26"] = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = df["ema12"] - df["ema26"]
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
        df["ma_diff"] = (df["close"] - df["ma"]) / df["ma"]
        df["volatility"] = df["high"] - df["low"]
        df["label"] = (df["close"].shift(-1) > df["close"]).astype(int)
        df.dropna(inplace=True)

        # 学習させる
        self.strategy.train_model(df)

        trades_today = 0
        for i in range(30, len(df)):
            if trades_today >= self.max_trades_per_day:
                break
            slice_df = df.iloc[:i+1]
            decision = self.strategy.should_trade(slice_df)
            if decision:
                entry_price = slice_df.iloc[-1]["close"]
                self.exchange.place_order("BTCUSDT", decision, 0.01, entry_price)
                trades_today += 1
                self.logger.log(f"[複合足] エントリー {decision} @ {entry_price:.2f}")

        result = self.exchange.close_all(entry_price)
        pnl = sum([r["pnl"] for r in result])
        self.logger.log(f"トレード終了: 損益 = {pnl:.2f}")

class TradeStrategy:
    def get_trade_signal(self):
        import random
        return random.choice(["buy", "sell", None])
