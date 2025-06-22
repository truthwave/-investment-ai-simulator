# filters.py

class TradeFilters:
    def __init__(self):
        self.daily_trade_count = {}
        self.max_trades_per_day = 10

    def allow_trade(self, candle, past_data):
        date = str(candle["datetime"].date())
        self.daily_trade_count.setdefault(date, 0)

        # 値動きが一定以上（ボラティリティ）で、取引数が上限以下
        if self.daily_trade_count[date] < self.max_trades_per_day and candle["high"] - candle["low"] > candle["close"] * 0.005:
            self.daily_trade_count[date] += 1
            return True
        return False
