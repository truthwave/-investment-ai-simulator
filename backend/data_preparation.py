# data_preparation.py

import pandas as pd
import talib
import os

def prepare_training_data():
    print("📊 学習データ準備を開始します...")

    df = pd.read_csv("btc_price_data.csv")

    # タイムスタンプ整形
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    # 必須列の欠損除去
    df.dropna(subset=["open", "high", "low", "close", "volume"], inplace=True)

    # ============ 追加するテクニカル指標（特徴量） ============

    df["rsi"] = talib.RSI(df["close"], timeperiod=14)
    df["ma"] = talib.SMA(df["close"], timeperiod=20)
    df["ma_50"] = talib.SMA(df["close"], timeperiod=50)
    df["ma_200"] = talib.SMA(df["close"], timeperiod=200)

    macd, macd_signal, macd_hist = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
    df["macd"] = macd
    df["macd_signal"] = macd_signal
    df["macd_histogram"] = macd_hist

    upper, middle, lower = talib.BBANDS(df["close"], timeperiod=20)
    df["bb_upper"] = upper
    df["bb_middle"] = middle
    df["bb_lower"] = lower
    df["bollinger_band_width"] = upper - lower

    df["volatility"] = df["high"] - df["low"]

    df["ma_diff"] = (df["close"] - df["ma"]) / df["ma"]
    df["ma_trend"] = df["ma"].diff()

    df["price_change"] = df["close"].pct_change()
   
    # 例：0.5%（0.005）以上の変化を検出対象とする
    df["target"] = (df["close"].shift(-1) > df["close"] * 1.005).astype(int)
   
    # 既存の DataFrame に追加する特徴量の計算
    df["price_range"] = df["high"] - df["low"]
    df["volatility_ratio"] = df["price_range"] / df["close"]

    # 移動平均の傾き（過去5本で変化量）
    df["ma_slope"] = df["ma"].diff(5)
    df["rsi_slope"] = df["rsi"].diff(5)

    # MACDヒストグラム
    df["macd_histogram"] = df["macd"] - df["macd_signal"]

    # 過去5本前と10本前からの騰落率
    df["return_5"] = (df["close"] - df["close"].shift(5)) / df["close"].shift(5)
    df["return_10"] = (df["close"] - df["close"].shift(10)) / df["close"].shift(10)

    # RSI変化率
    df["rsi_change"] = df["rsi"].diff()

    # 過去数本の終値平均（短期の価格動向）
    df["close_mean_3"] = df["close"].rolling(window=3).mean()

    # ボリンジャーバンド幅
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]
    df["rsi_volatility_combo"] = df["rsi"] * df["volatility"]
    df["macd_diff"] = df["macd"] - df["macd_signal"]
   
    df['ma_ratio'] = df['ma'] / (df['close_mean_3'] + 1e-9)
    df['rsi_macd_diff'] = df['rsi'] - df['macd']
    df['vol_bb_ratio'] = df['volatility'] / (df['bb_width'] + 1e-9)


    
    df.dropna(inplace=True)

    # 保存
    df.to_csv("training_data.csv", index=False)

    print(f"✅ 学習用データ保存完了: training_data.csv（{len(df)}行）")
    print(df["target"].value_counts())

if __name__ == "__main__":
    prepare_training_data()
