# ==========================
# symbol_fetcher.py
# 最新のS&P500/NASDAQ/日経平均銘柄リストを取得（INDEX_SOURCE対応）
# ==========================

import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

# S&P500（セクター付き）
def fetch_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'id': 'constituents'})
    html_str = str(table)
    df = pd.read_html(StringIO(html_str))[0]
    return df['Symbol'].tolist()

# NASDAQ100
def fetch_nasdaq100_symbols():
    url = 'https://finance.yahoo.com/quote/%5ENDX/components/'
    response = requests.get(url)
    tables = pd.read_html(response.text)
    df = tables[0]
    return df['Symbol'].tolist()

# 日経平均225
def fetch_nikkei225_symbols():
    url = 'https://ja.wikipedia.org/wiki/日経平均株価'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = pd.read_html(str(soup))
    df = next((t for t in tables if 'コード' in t.columns), None)
    if df is None:
        return []
    return [str(code).zfill(4) + ".T" for code in df['コード'].tolist()]

# ==========================
# メイン関数：INDEX_SOURCEに応じて銘柄リストを返す
# ==========================
def fetch_symbols(index_source):
    index_source = index_source.lower()
    if index_source == "sp500":
        return fetch_sp500_symbols()
    elif index_source == "nasdaq100":
        return fetch_nasdaq100_symbols()
    elif index_source == "nikkei225":
        return fetch_nikkei225_symbols()
    else:
        raise ValueError(f"未対応のインデックス指定: {index_source}")
