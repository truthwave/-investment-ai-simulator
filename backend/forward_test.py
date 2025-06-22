import time
from backend.trading_manager import TradingManager

# フォワードテストの実行設定
INTERVAL = 60 * 5  # 5分ごと
DURATION_HOURS = 24  # テスト実行時間（例: 24時間）

# TradingManager のインスタンスを作成
manager = TradingManager(mode="virtual")  # 仮想取引用

end_time = time.time() + DURATION_HOURS * 3600

while time.time() < end_time:
    print("=== フォワードテスト取引開始 ===")
    try:
        manager.run_strategy()  # 戦略実行（取引が発生すればログに記録）
    except Exception as e:
        print(f"エラー: {e}")
    time.sleep(INTERVAL)
