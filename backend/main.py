# ==========================
# 必要ライブラリ読み込み・初期設定
# ==========================
import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from io import StringIO
from collections import defaultdict
import re
import logging
from get_stock_data import get_price_data
from portfolio_module import Portfolio
from symbols_loader import fetch_sp500_symbols, fetch_nikkei225_symbols
from signal_calculator import calculate_indicators, generate_signal
from utils import log
import logging
# ==========================
# ログ設定（コンソール＋ファイル）
# ==========================
LOG_FILE = 'run_log.txt'
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
# ==========================
# ポートフォリオ初期化
# ==========================
portfolio = Portfolio()

# ==========================
# 市場スキャン処理
# ==========================
logger = logging.getLogger(__name__)

def scan_market():
    """
    市場をスキャンし、長期投資の売買判断を行う
    """
    logger.info("銘柄リストを取得中...")
    symbols = fetch_sp500_symbols() + fetch_nikkei225_symbols()
    
    portfolio = Portfolio()

    for symbol in symbols:
        logger.info(f"スキャン中: {symbol}")
        df = get_price_data(symbol)

        if df is None or df.empty:
            logger.warning(f"[データ取得エラー] {symbol} のデータが取得できません")
            continue

        try:
            df = calculate_indicators(df)
        except Exception as e:
            logger.error(f"[指標計算エラー] {symbol}: {e}")
            continue

        # 売買判断
        if symbol in portfolio.positions:
            entry_price = portfolio.positions[symbol]
            signal, reason = generate_signal(df, symbol, entry_price)

            if signal == "sell":
                portfolio.sell(symbol, df['Close'].iloc[-1])
                logger.info(f"[SELL] {symbol}: {reason}")

if __name__ == "__main__":
    scan_market()

def is_valid_symbol(symbol: str) -> bool:
    # アルファベット、数字、「.」「-」のみ許可（%や空白などを除外）
    return bool(re.match(r'^[A-Z0-9.\-]+$', symbol))
# ==========================
# 実行
# ==========================
if __name__ == "__main__":
    scan_market()

# ==========================
# 補助関数
# ==========================
def is_valid_symbol(symbol: str) -> bool:
    return bool(re.match(r'^[A-Z0-9.\-]+$', symbol))
