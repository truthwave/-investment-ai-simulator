import yfinance as yf
import pandas as pd
from backend.trade_history import TradeHistory
from typing import Dict, Union, Optional

class TradeLogic:
    """株価データを分析し、売買シグナルを生成するクラス"""

    RSI_OVERBOUGHT = 70  # RSI買われすぎ水準
    RSI_OVERSOLD = 30   # RSI売られすぎ水準
    RSI_PERIOD = 14     # RSI計算期間

    def __init__(self):
        self.trade_history = TradeHistory()
        self.max_trades_per_day = 10  # 1日10銘柄制限
        self.traded_stocks = []

    def get_stock_data(self, ticker: str) -> Union[pd.DataFrame, Dict[str, str]]:
        """指定した銘柄の株価データを取得

        Args:
            ticker (str): ティッカーシンボル

        Returns:
            Union[pd.DataFrame, Dict[str, str]]: 株価データまたはエラーメッセージ
        """
        data = yf.download(ticker, period="1mo", interval="1h")
        if data.empty:
            return {"status": "エラー", "message": "株価データが取得できませんでした。"}
        return data

    def analyze(self, ticker: str, quantity: int = 1) -> str:
        """売買判断を行い、取引履歴に記録

        Args:
            ticker (str): ティッカーシンボル
            quantity (int, optional): 取引数量. Defaults to 1.

        Returns:
            str: 売買シグナル (BUY, SELL, HOLD)
        """
        if len(self.traded_stocks) >= self.max_trades_per_day:
            return "HOLD"

        data = self.get_stock_data(ticker)
        if isinstance(data, dict) and "status" in data:
            return data

        try:
            # VWAP, RSI 計算
            data["RSI"] = self.calculate_rsi(data)
            volume_cumsum = data["Volume"].cumsum()
            vwap = (data["Close"] * data["Volume"]).cumsum() / volume_cumsum
            latest_price = float(data["Close"].iloc[-1])
            rsi = float(data["RSI"].iloc[-1])
            vwap_last = float(vwap.iloc[-1])  # 例外処理を追加
        except (IndexError, ValueError) as e:
            return {"status": "エラー", "message": f"データ処理中にエラーが発生しました: {e}"}

        # 売買ロジック
        if latest_price < vwap_last and rsi < self.RSI_OVERSOLD:
            self.traded_stocks.append(ticker)
            self.trade_history.log_trade(ticker, "BUY", latest_price, quantity)
            return "BUY"
        elif rsi > self.RSI_OVERBOUGHT:
            self.traded_stocks.append(ticker)
            self.trade_history.log_trade(ticker, "SELL", latest_price, quantity)
            return "SELL"
        else:
            return "HOLD"

    def calculate_rsi(self, data: pd.DataFrame, period: int = RSI_PERIOD) -> pd.Series:
        """RSIを計算

        Args:
            data (pd.DataFrame): 株価データ
            period (int, optional): RSI計算期間. Defaults to RSI_PERIOD.

        Returns:
            pd.Series: RSI
        """
        delta = data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))