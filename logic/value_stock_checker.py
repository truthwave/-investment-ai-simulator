# backend/logic/value_stock_checker.py

def is_value_stock(stock: dict) -> bool:
    """
    バフェット式バリュー株かどうかを判定する
    :param stock: 株式情報の辞書（PER, PBR, ROEなどを含む）
    :return: True=割安株, False=対象外
    """
    try:
        per = float(stock.get("per", 0))
        pbr = float(stock.get("pbr", 0))
        roe = float(stock.get("roe", 0))
        equity_ratio = float(stock.get("equity_ratio", 0))
        dividend_yield = float(stock.get("dividend_yield", 0))

        if per <= 15 and pbr <= 1.5 and roe >= 10 and equity_ratio >= 40 and dividend_yield >= 3:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] 評価時エラー: {e}")
        return False
