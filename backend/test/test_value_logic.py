# backend/test/test_value_logic.py

from backend.logic.value_stock_checker import is_value_stock

# テストデータ
test_stock = {
    "ticker": "9984",
    "name": "ソフトバンクグループ",
    "per": 12.5,
    "pbr": 1.2,
    "roe": 11.0,
    "equity_ratio": 45.3,
    "dividend_yield": 3.2
}

if is_value_stock(test_stock):
    print(f"{test_stock['name']}（{test_stock['ticker']}）は割安株です。")
else:
    print(f"{test_stock['name']}（{test_stock['ticker']}）は割安株ではありません。")
