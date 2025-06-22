# ==========================
# daily_report.py
# 1日の取引まとめレポート通知＋資金推移グラフ送信
# ==========================

import pandas as pd
import matplotlib.pyplot as plt
import os
from notifier import send_trade_signal, send_trade_signal_with_image
from datetime import datetime

HISTORY_FILE = 'trade_history.csv'
BALANCE_IMAGE = 'balance_plot.png'

def send_daily_report():
    if not os.path.exists(HISTORY_FILE):
        send_trade_signal(subject="【日次レポート】", body="本日の取引履歴はありませんでした。")
        return

    df = pd.read_csv(HISTORY_FILE)

    today = datetime.now().strftime("%Y-%m-%d")
    df_today = df[df['date'] == today]

    if df_today.empty:
        send_trade_signal(subject="【日次レポート】", body="本日の取引履歴はありませんでした。")
        return

    entry_count = df_today[df_today['type'] == 'entry'].shape[0]
    exit_count = df_today[df_today['type'] == 'exit'].shape[0]
    profit_total = df_today[df_today['type'] == 'exit']['profit'].sum()

    report = (
        f"【本日の取引サマリー】\n"
        f"・エントリー回数: {entry_count}回\n"
        f"・イグジット回数: {exit_count}回\n"
        f"・本日合計損益: {profit_total:.2f}円\n"
    )

    send_trade_signal(subject="【日次取引レポート】", body=report)

    # 資金推移グラフ作成
    df_exit = df[df['type'] == 'exit'].copy()
    df_exit['cumulative_profit'] = df_exit['profit'].cumsum()
    df_exit['virtual_balance'] = 10000 + df_exit['cumulative_profit']

    plt.figure(figsize=(10,6))
    plt.plot(df_exit['date'], df_exit['virtual_balance'], marker='o')
    plt.title('仮想資金推移')
    plt.xlabel('日付')
    plt.ylabel('仮想資金額（円）')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(BALANCE_IMAGE)
    plt.close()

    # グラフ画像送信
    send_trade_signal_with_image(
        subject="【資金推移グラフ】",
        body="現在の仮想資金推移をご確認ください！",
        image_path=BALANCE_IMAGE
    )
