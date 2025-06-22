import pandas as pd
from backtest_engine import BacktestEngine
import itertools
from notifier import send_email

# 検証パラメータ範囲
entry_threshold_list = [1.5, 2.0, 2.5]
tp_multiplier_list = [1.5, 2.0, 2.5]
sl_multiplier_list = [0.5, 1.0, 1.5]

# データ読み込み
def load_price_data(filepath):
    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

# strategy_config.py に書き込む
def write_best_to_config(best_result, filename="strategy_config.py"):
    content = f"""# 自動最適化により更新されたパラメータ

entry_threshold = {best_result['entry_threshold']}
take_profit_atr_multiplier = {best_result['tp_multiplier']}
stop_loss_atr_multiplier = {best_result['sl_multiplier']}

trend_adx_threshold = 25
box_adx_threshold = 40
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n💾 strategy_config.py を更新しました（{filename}）")

# メイン処理（✅ すべてここで完結）
def main():
    df = load_price_data("data/historical_price.csv")
    results = []

    for entry_threshold, tp, sl in itertools.product(entry_threshold_list, tp_multiplier_list, sl_multiplier_list):
        engine = BacktestEngine(
            entry_threshold=entry_threshold,
            take_profit_atr_multiplier=tp,
            stop_loss_atr_multiplier=sl
        )
        result = engine.run(df)

        results.append({
            "entry_threshold": entry_threshold,
            "tp_multiplier": tp,
            "sl_multiplier": sl,
            "final_balance": result["final_balance"],
            "profit": result["profit"],
            "win_rate": result["win_rate"],
            "sharpe_ratio": result["sharpe_ratio"],
            "max_drawdown": result["max_drawdown"]
        })

    results.sort(key=lambda x: x["sharpe_ratio"], reverse=True)
    best = results[0]

    print("\n✅ 最良パラメータ:")
    print(f"entry={best['entry_threshold']}, TPxATR={best['tp_multiplier']}, SLxATR={best['sl_multiplier']}")
    print(f"Profit={best['profit']:.2f}, Sharpe={best['sharpe_ratio']:.2f}, WinRate={best['win_rate']:.2f}%, DD={best['max_drawdown']:.2f}%")

    write_best_to_config(best)

    message = (
        f"[戦略パラメータ最適化 完了]\n\n"
        f"entry_threshold: {best['entry_threshold']}\n"
        f"TPxATR: {best['tp_multiplier']}\n"
        f"SLxATR: {best['sl_multiplier']}\n\n"
        f"Profit: ¥{best['profit']:.2f}\n"
        f"Sharpe Ratio: {best['sharpe_ratio']:.2f}\n"
        f"Win Rate: {best['win_rate']:.2f}%\n"
        f"Max Drawdown: {best['max_drawdown']:.2f}%"
    )
    send_email("📈 自動最適化完了通知", message)

# エントリーポイント
if __name__ == "__main__":
    main()
