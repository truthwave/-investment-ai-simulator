# virtual_backtest.py

import csv
import random
from datetime import datetime, timedelta
import os

DAYS = 7
START_PRICE = 50000
INITIAL_USDT = 1000
TRADE_AMOUNT_RATIO = 0.1  # 資金の10%を使って複利運用
TAKE_PROFIT_PCT = 0.02
STOP_LOSS_PCT = -0.01

LOG_PATH = "logs/virtual_results.csv"

def generate_fake_market_data():
    """過去7日分のOHLCVとRSI, MAを含むダミーデータを作成"""
    prices = []
    for _ in range(DAYS + 14):  # RSI, MAのため余分に
        open_price = round(START_PRICE * random.uniform(0.97, 1.03), 2)
        close_price = round(open_price * random.uniform(0.98, 1.02), 2)
        high = max(open_price, close_price) * random.uniform(1.00, 1.02)
        low = min(open_price, close_price) * random.uniform(0.98, 1.00)
        prices.append({
            "open": open_price,
            "close": close_price,
            "high": round(high, 2),
            "low": round(low, 2)
        })
    return prices

def calculate_rsi(prices, period=14):
    rsis = [None]*period
    for i in range(period, len(prices)):
        gains = []
        losses = []
        for j in range(i - period, i):
            diff = prices[j+1]["close"] - prices[j]["close"]
            if diff >= 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 1e-6
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsis.append(round(rsi, 2))
    return rsis

def calculate_ma(prices, period=5):
    mas = [None]*(period-1)
    for i in range(period-1, len(prices)):
        ma = sum([p["close"] for p in prices[i-period+1:i+1]]) / period
        mas.append(round(ma, 2))
    return mas

def simulate_virtual_trading():
    os.makedirs("logs", exist_ok=True)
    prices = generate_fake_market_data()
    rsis = calculate_rsi(prices)
    mas = calculate_ma(prices)

    current_balance = INITIAL_USDT
    trade_count = 0  # ここで初期化
    win_count = 0    # ここで初期化
    lose_count = 0   # ここで初期化

    with open(LOG_PATH, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "entry", "exit", "RSI", "MA", "entry_price", "exit_price", "profit_pct", "balance"])

        for i in range(14, 14 + DAYS):
            date = (datetime.now() - timedelta(days=(DAYS - (i - 14)))).strftime("%Y-%m-%d")
            rsi = rsis[i]
            ma = mas[i]
            price_data = prices[i]

            entry_price = price_data["open"]
            position = None

            # テクニカル条件でエントリー
            if rsi and ma:
                if rsi < 30 and entry_price > ma:
                    position = "buy"
                elif rsi > 70 and entry_price < ma:
                    position = "sell"

            if not position:
                writer.writerow([date, None, None, rsi, ma, None, None, 0, round(current_balance, 2)])
                continue

            take_profit = entry_price * (1 + TAKE_PROFIT_PCT) if position == "buy" else entry_price * (1 - TAKE_PROFIT_PCT)
            stop_loss = entry_price * (1 + STOP_LOSS_PCT) if position == "buy" else entry_price * (1 - STOP_LOSS_PCT)

            trade_amount = current_balance * TRADE_AMOUNT_RATIO
            coin_amount = trade_amount / entry_price

            # 決済価格決定
            if position == "buy":
                if price_data["high"] >= take_profit:
                    exit_price = take_profit
                elif price_data["low"] <= stop_loss:
                    exit_price = stop_loss
                else:
                    exit_price = price_data["close"]
                profit = (exit_price - entry_price) * coin_amount
            else:
                if price_data["low"] <= take_profit:
                    exit_price = take_profit
                elif price_data["high"] >= stop_loss:
                    exit_price = stop_loss
                else:
                    exit_price = price_data["close"]
                profit = (entry_price - exit_price) * coin_amount

            current_balance += profit
            profit_pct = (profit / trade_amount) * 100

            writer.writerow([date, position, "close", rsi, ma,
                             round(entry_price, 2), round(exit_price, 2),
                             round(profit_pct, 2), round(current_balance, 2)])
    
    print("\n--- バックテスト結果 ---")
    print(f"初期資金: {INITIAL_USDT:.2f} USDT")
    print(f"最終資金: {current_balance:.2f} USDT")
    profit_loss = current_balance - INITIAL_USDT
    profit_loss_pct = (profit_loss / INITIAL_USDT) * 100
    print(f"損益: {profit_loss:.2f} USDT ({profit_loss_pct:.2f}%)")
    print(f"取引回数: {trade_count}")
    if trade_count > 0:
        win_rate = (win_count / trade_count) * 100
        print(f"勝率: {win_rate:.2f}%")
        print(f"勝ち数: {win_count}")
        print(f"負け数: {lose_count}")
    else:
        print("取引なし")
    print(f"ログファイル: {LOG_PATH}")

if __name__ == "__main__":
    simulate_virtual_trading()
