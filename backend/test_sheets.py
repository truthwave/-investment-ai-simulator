# ==========================
# test_sheets.py
# Google Sheetsテスト書き込み
# ==========================

from sheets_service import get_worksheet
from datetime import datetime

# スプレッドシートへ直接行を追加する関数
def write_test_signal():
    worksheet = get_worksheet()

    now = datetime.now()
    date_str = now.strftime("25-004-28")  # 今日の日付
    time_str = now.strftime("08:22:30")  # 今の時刻

    # 書き込むデータ（あなたが希望した内容）
    row = [
        date_str,  # 今日の日付
        time_str,  # 今の時刻
        'entry',   # 固定文字列
        'TEST',    # 銘柄シンボル
        123.45     # 価格
    ]

    # 行を追加
    worksheet.append_row(row)
    print("✅ テストデータ書き込み完了！")

# 実行
if __name__ == "__main__":
    write_test_signal()
