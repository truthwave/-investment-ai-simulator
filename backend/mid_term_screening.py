import pandas as pd

# パート1：中期投資向けスクリーニング関数
def screen_mid_term_candidates(csv_path="stocks.csv"):
    df = pd.read_csv(csv_path)

    # 必要な列が揃っているかチェック
    required_columns = ["銘柄名", "時価総額", "営業利益率", "売上高成長率", "ROE", "PER"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("CSVに必要な列が含まれていません。")

    # スクリーニング条件
    filtered = df[
        (df["時価総額"] >= 500e8) &
        (df["営業利益率"] >= 10) &
        (df["売上高成長率"] >= 10) &
        (df["ROE"] >= 10) &
        (df["PER"] <= 20)
    ]

    return filtered
