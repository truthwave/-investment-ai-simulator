# symbols_loader.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from utils import log

def fetch_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    html_table = str(table)  # テーブルをHTML文字列化
    df = pd.read_html(StringIO(html_table))[0]  # ← ここでStringIOを使うのが重要
    symbols = df['Symbol'].tolist()
    symbols = [s.replace('.', '-') for s in symbols]
    return symbols

def fetch_nikkei225_symbols():
    try:
        url = 'https://indexes.nikkei.co.jp/nkave/index/component?idx=nk225'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if table is None:
            log("[エラー] テーブルが見つかりません")
            return []

        df = pd.read_html(StringIO(str(table)))[0]
        if 'コード' not in df.columns:
            log("[エラー] 'コード' 列が見つかりません")
            return []

        symbols = df['コード'].astype(str).tolist()
        symbols = [s + '.T' for s in symbols]
        return symbols

    except Exception as e:
        log(f"[エラー] 日経225銘柄取得失敗: {e}")
        return []


