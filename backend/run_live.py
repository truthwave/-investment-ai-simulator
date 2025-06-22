# run_live.py

from backend.trading_manager import TradingManager

def main():
    print("=== 複数時間足AIトレード開始 ===")

    manager = TradingManager()

    try:
        manager.run_strategy()  # run_strategy() は複数時間足対応版にしておく
        print("トレード処理完了（1回分）")
    except Exception as e:
        print(f"[エラー発生] {e}")

if __name__ == '__main__':
    main()
