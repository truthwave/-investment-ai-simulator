import csv
import os

# CSVファイルのパス（取引履歴を保存）
CSV_FILE = "trade_history.csv"

# 取引をCSVに保存する関数
def save_trade_to_csv(timestamp, symbol, side, price, quantity, profit_loss, order_id):
    # CSVのヘッダー
    header = ["日時", "銘柄", "売買", "価格", "数量", "損益", "注文ID"]
    data = [timestamp, symbol, side, price, quantity, profit_loss, order_id]
    
    # ファイルが存在しない場合はヘッダーを追加
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # ヘッダーを書き込み
        writer.writerow(data)  # 取引データを書き込み

    print(f"✅ 取引記録をCSVに保存: {data}")

# テスト: 取引を記録
save_trade_to_csv("2025-03-26 09:45", "AAPL", "買い", 224.76, 10, "-", "001")
save_trade_to_csv("2025-03-26 10:15", "AAPL", "売り", 225.90, 10, "+11.4", "001")
