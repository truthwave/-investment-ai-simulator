# ==========================
# symbol_filter.py
# 銘柄フィルタリングモジュール
# ==========================

import yfinance as yf

# ==========================
# フィルタリング関数
# ==========================
def filter_symbols(df_sp500, nasdaq_symbols, nikkei_symbols, 
                   target_sectors, price_threshold=10):
    """
    指定セクターと株価条件でフィルタリング
    :param df_sp500: S&P500銘柄DataFrame（セクター付き）
    :param nasdaq_symbols: NASDAQ銘柄リスト
    :param nikkei_symbols: 日経平均銘柄リスト
    :param target_sectors: 対象セクターリスト
    :param price_threshold: 最低株価
    :return: フィルタ後のシンボルリスト
    """

    # --- 1. S&P500から対象セクター銘柄抽出 ---
    df_filtered = df_sp500[df_sp500['Sector'].isin(target_sectors)]
    symbols = df_filtered['Symbol'].tolist()

    # --- 2. NASDAQ/NIKKEI銘柄をマージ（セクターなし） ---
    symbols += nasdaq_symbols
    symbols += nikkei_symbols

    # --- 3. 重複排除 ---
    symbols = list(set(symbols))

    # --- 4. 株価フィルター（10ドル以上） ---
    final_symbols = []
    for symbol in symbols:
        try:
            data = yf.Ticker(symbol)
            price = data.history(period="1d")['Close'].iloc[-1]
            if price >= price_threshold:
                final_symbols.append(symbol)
        except Exception:
            continue

    return final_symbols
