import pandas as pd

def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    return macd, macd_signal

def enrich_with_features(df):
    df['rsi'] = calculate_rsi(df['close'])
    df['ma'] = df['close'].rolling(window=14).mean()
    df['ma_diff'] = (df['close'] - df['ma']) / df['ma']
    df['volatility'] = df['high'] - df['low']
    df['macd'], df['macd_signal'] = calculate_macd(df['close'])
    df['label'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.dropna(inplace=True)
    return df

# 実行部分
raw_df = pd.read_csv("btc_price_data.csv")  # ※ 既にこのファイルが必要です
df = enrich_with_features(raw_df)
df.to_csv("btc_train_ready.csv", index=False)
print("btc_train_ready.csv を作成しました。")
