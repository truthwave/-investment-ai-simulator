import pandas as pd
import argparse
import matplotlib.pyplot as plt
import pprint

from backtest_engine import BacktestEngine
import strategy_config as config

def load_price_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)
        return df
    except Exception as e:
        print(f"📛 データ読み込み失敗: {e}")
        exit(1)

def main():
    print("🚀 バックテスト開始")

    parser = argparse.ArgumentParser(description="バックテストを実行します")
    parser.add_argument("--data", default="data/historical_price.csv", help="CSVデータファイルのパス")
    args = parser.parse_args()

    df = load_price_data(args.data)

    # ✅ lot_size & 複利パラメータも strategy_config から取得
    engine = BacktestEngine(
        entry_threshold=config.entry_threshold,
        take_profit_atr_multiplier=config.take_profit_atr_multiplier,
        stop_loss_atr_multiplier=config.stop_loss_atr_multiplier,
        lot_size=config.lot_size,
        use_compounding=config.use_compounding
    )

    result = engine.run(df)

    print("📈 バックテスト結果")
    print(f"初期資金: {result['initial_balance']:,} 円")
    print(f"最終評価額: {result['final_balance']:.2f} 円")
    print(f"損益: {result['profit']:.2f} 円")
    print(f"勝率: {result['win_rate']:.2f}%")
    print(f"最大ドローダウン: {result['max_drawdown']:.2f}%")
    print(f"シャープレシオ: {result['sharpe_ratio']:.2f}")
    print("取引履歴:")
    pprint.pprint(result["trades"])

    plt.plot(result["balance_history"])
    plt.title("Equity Curve")
    plt.xlabel("Trade #")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.savefig("equity_curve.png")
    print("📊 損益曲線を equity_curve.png に保存しました。")

if __name__ == "__main__":
    main()
