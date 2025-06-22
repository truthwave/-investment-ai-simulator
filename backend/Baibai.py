import csv
import os

CSV_FILE = "trade_history.csv"

# 保持しているポジション（仮想的なエントリーリスト）
open_positions = []

# 取引をCSVに保存する関数
def save_trade_to_csv(timestamp, symbol, side, price, quantity, profit_loss, order_id):
    header = ["日時", "銘柄", "売買", "価格", "数量", "損益", "注文ID"]
    data = [timestamp, symbol, side, price, quantity, profit_loss, order_id]
    
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(data)

    print(f"✅ 取引記録をCSVに保存: {data}")

# 仮想エントリー（買い注文）
def enter_trade(timestamp, symbol, price, quantity, order_id, tp=0.02, sl=0.05):
    global open_positions
    take_profit_price = price * (1 + tp)  # 利確ライン
    stop_loss_price = price * (1 - sl)  # 損切りライン

    open_positions.append({
        "timestamp": timestamp,
        "symbol": symbol,
        "buy_price": price,
        "quantity": quantity,
        "order_id": order_id,
        "tp": take_profit_price,
        "sl": stop_loss_price
    })
    
    save_trade_to_csv(timestamp, symbol, "買い", price, quantity, "-", order_id)
    print(f"🔼 仮想買い注文: {symbol} @ {price} 数量: {quantity} (TP: {take_profit_price}, SL: {stop_loss_price})")

# 仮想エグジット（売り注文）
def exit_trade(timestamp, symbol, current_price):
    global open_positions
    new_positions = []

    for trade in open_positions:
        if trade["symbol"] == symbol:
            if current_price >= trade["tp"]:
                profit_loss = (trade["tp"] - trade["buy_price"]) * trade["quantity"]
                save_trade_to_csv(timestamp, symbol, "売り (利確)", trade["tp"], trade["quantity"], profit_loss, trade["order_id"])
                print(f"✅ 利確: {symbol} @ {trade['tp']} 損益: {profit_loss}")
            elif current_price <= trade["sl"]:
                profit_loss = (trade["sl"] - trade["buy_price"]) * trade["quantity"]
                save_trade_to_csv(timestamp, symbol, "売り (損切り)", trade["sl"], trade["quantity"], profit_loss, trade["order_id"])
                print(f"❌ 損切り: {symbol} @ {trade['sl']} 損益: {profit_loss}")
            else:
                new_positions.append(trade)  # まだ決済しない場合は残す
        else:
            new_positions.append(trade)

    open_positions = new_positions

# 📌 仮想売買テスト
enter_trade("2025-03-26 09:45", "AAPL", 224.76, 10, "001")  # 買い注文
exit_trade("2025-03-26 10:15", "AAPL", 229.00)  # 売り注文（利確ライン到達）
exit_trade("2025-03-26 10:30", "AAPL", 213.00)  # 売り注文（損切りライン到達）
