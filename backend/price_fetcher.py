# backend/price_fetcher.py
import yfinance as yf

def get_price(ticker: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")  # 直近1日のデータ
    if not data.empty:
        latest = data.iloc[-1]
        return {
            "ticker": ticker,
            "price": latest["Close"],
            "volume": latest["Volume"]
        }
    else:
        return {"error": "データ取得失敗"}
