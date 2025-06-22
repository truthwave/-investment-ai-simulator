# backend/stock_filter.py

import pandas as pd

# スクリーニング条件を適用してフィルター処理を行う関数
def screen_stocks(file_path: str = "stocks.csv"):
    try:
        df = pd.read_csv(file_path)

        # 必須列の存在チェック
        required_columns = ["売上成長率", "EPS成長率", "PER", "ROE", "ティッカー"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSVファイルに必要な列が不足しています。")

        # 条件に合致する行を抽出
        filtered_df = df[
            (df["売上成長率"] >= 10) &
            (df["EPS成長率"] >= 10) &
            (df["PER"] <= 15) &
            (df["ROE"] >= 10)
        ]

        # 結果を辞書のリストとして返す
        return filtered_df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
