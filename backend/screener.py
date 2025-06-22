# backend/screener.py
import pandas as pd
from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/screening/midterm")
def screen_stocks():
    # プロジェクトルートにある CSV ファイルのパスを解決
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stocks.csv"))
    
    # ファイルが存在しない場合のエラー処理
    if not os.path.isfile(csv_path):
        return {"status": "error", "message": f"ファイルが存在しません: {csv_path}"}

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return {"status": "error", "message": f"CSV読み込みエラー: {str(e)}"}

    # データ型の確認と変換（文字列→float）
    for col in ["売上成長率", "EPS成長率", "PER", "ROE"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 条件フィルター
    filtered = df[
        (df["売上成長率"] >= 10) &
        (df["EPS成長率"] >= 10) &
        (df["PER"] <= 15) &
        (df["ROE"] >= 10)
    ]

    return {
        "status": "success",
        "count": len(filtered),
        "results": filtered[["ティッカー", "売上成長率", "EPS成長率", "PER", "ROE"]].to_dict(orient="records")
    }
