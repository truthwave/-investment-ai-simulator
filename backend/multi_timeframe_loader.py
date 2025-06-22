import pandas as pd

def load_candles(timeframe):
    filename = f"candles_{timeframe}.csv"
    df = pd.read_csv(filename)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df

def merge_timeframes(df_short, df_long):
    df_long = df_long[["close", "ma", "macd", "macd_signal"]]
    df_long.columns = [f"{col}_long" for col in df_long.columns]
    merged = pd.merge_asof(df_short.sort_index(), df_long.sort_index(),
                           left_index=True, right_index=True, direction="backward")
    return merged
