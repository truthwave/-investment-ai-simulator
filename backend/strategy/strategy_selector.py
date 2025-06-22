# strategy_selector.py

from .trend_strategy import TrendStrategy
from .range_strategy import RangeStrategy
from .box_strategy import BoxStrategy

class StrategySelector:
    def __init__(
        self,
        trend_adx_threshold=25,
        box_adx_threshold=40,
        entry_threshold=2.0,
        take_profit_atr_multiplier=2.0,
        stop_loss_atr_multiplier=1.0
    ):
        self.trend_adx_threshold = trend_adx_threshold
        self.box_adx_threshold = box_adx_threshold

        # 各戦略インスタンスの生成
        self.trend_strategy = TrendStrategy(entry_threshold=entry_threshold)
        self.range_strategy = RangeStrategy(entry_threshold=entry_threshold)
        self.box_strategy = BoxStrategy()  # entry_threshold 不使用なら不要

        self.take_profit_atr_multiplier = take_profit_atr_multiplier
        self.stop_loss_atr_multiplier = stop_loss_atr_multiplier

    # パート1：インジケーターを全戦略に反映
    def calculate_indicators(self, df):
        """
        各戦略が必要とするインジケーターを計算してDataFrameに追加
        """
        df = self.trend_strategy.calculate_indicators(df)
        df = self.range_strategy.calculate_indicators(df)  # ✅ 追加必要
        df = self.box_strategy.calculate_indicators(df)
        return df

    # パート2：マーケットタイプの判定
    def determine_market_type(self, df):
        """
        ADXに基づき相場タイプを判定：
        - ADX >= box_adx_threshold：ボックス相場
        - ADX >= trend_adx_threshold：トレンド相場
        - ADX < trend_adx_threshold：レンジ相場
        """
        if len(df) < 35:
            return "unknown"

        latest_adx = df["adx"].iloc[-1]
        if latest_adx >= self.box_adx_threshold:
            return "box"
        elif latest_adx >= self.trend_adx_threshold:
            return "trend"
        else:
            return "range"

    # パート3：エントリー判断
    def should_trade(self, df):
        """
        市場タイプに応じた戦略でエントリー判断を行う
        """
        market_type = self.determine_market_type(df)
        if market_type == "trend":
            return self.trend_strategy.should_trade(df)
        elif market_type == "range":
            return self.range_strategy.should_trade(df)
        elif market_type == "box":
            return self.box_strategy.should_trade(df)
        return False  # ✅ None よりも False が妥当（ブール型を期待）

    # パート4：イグジット判断
    def should_exit(self, position, df):
        """
        市場タイプに応じた戦略でイグジット判断を行う
        """
        market_type = self.determine_market_type(df)

        if market_type == "trend":
            return self.trend_strategy.should_exit(
                position, df,
                self.take_profit_atr_multiplier,
                self.stop_loss_atr_multiplier
            )
        elif market_type == "range":
            return self.range_strategy.should_exit(
                position, df,
                self.take_profit_atr_multiplier,
                self.stop_loss_atr_multiplier
            )
        elif market_type == "box":
            # BoxStrategy に take_profit/stop_loss が必要なら渡すべき
            return self.box_strategy.should_exit(position, df)

        return False
