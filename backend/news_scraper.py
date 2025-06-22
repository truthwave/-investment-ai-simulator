import requests
from bs4 import BeautifulSoup

class NewsScraper:
    def __init__(self):
        self.urls = [
            "https://www.cnbc.com/world/",   # ✅ OK
            "https://www.nikkei.com/",       # ✅ OK（日本経済新聞）
            "https://finance.yahoo.com/"     # ✅ OK（Yahoo Finance）
        ]

    def fetch_news(self):
        news_data = []
        for url in self.urls:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    print(f"エラー: {url} - ステータスコード {response.status_code}")
                    continue
                soup = BeautifulSoup(response.content, "html.parser")
                headlines = soup.find_all("h2", limit=5)
                for headline in headlines:
                    if headline.text.strip():
                        news_data.append({
                            "source": url,
                            "title": headline.text.strip()
                        })
            except Exception as e:
                print(f"エラー: {e}")
        return news_data
