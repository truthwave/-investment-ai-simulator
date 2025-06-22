import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY") or "YOUR_API_KEY"
BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_fundamentals(symbol):
    url = f"{BASE_URL}/ratios-ttm/{symbol}?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()[0]

        fundamentals = {
            "PE_ratio": float(data.get("peRatioTTM", 0)),
            "ROE": float(data.get("roeTTM", 0)),
            "EPS": float(data.get("epsTTM", 0))
        }

        return fundamentals
    except Exception as e:
        print(f"API取得エラー: {e}")
        return None
