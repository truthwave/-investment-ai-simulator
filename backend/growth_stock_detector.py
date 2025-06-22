# backend/growth_stock_detector.py

import pandas as pd

def detect_growth_stocks(csv_path="stocks.csv"):
    df = pd.read_csv(csv_path)

    # 必須カラムの存在確認
    required = ["売上成長率", "EPS成長率", "PER", "ROE", "ティッカー"]
    if not all(col in df.columns for col in required):
        raise ValueError("必要なカラムがCSVに含まれていません")

    # 成長株の条件
    condition = (
        (df["売上成長率"] > 10) &
        (df["EPS成長率"] > 10) &
        (df["PER"] < 30) &
        (df["ROE"] > 15)
    )

    matched = df[condition]
    return matched[["ティッカー", "売上成長率", "EPS成長率", "PER", "ROE"]]
