# ==========================
# scheduler.py
# 毎日複数回＋日次レポート送信スケジューラー
# ==========================

import schedule
import time
import subprocess

TARGET_SCRIPT = 'main.py'
DAILY_REPORT_SCRIPT = 'daily_report.py'

def run_main_script():
    print("===== main.pyを実行します =====")
    try:
        subprocess.run(["python", TARGET_SCRIPT], check=True)
        print("===== 実行完了 =====")
    except subprocess.CalledProcessError as e:
        print(f"【エラー発生】main.py実行失敗：{e}")

def run_daily_report():
    print("===== 日次レポートを送信します =====")
    try:
        subprocess.run(["python", DAILY_REPORT_SCRIPT], check=True)
        print("===== レポート送信完了 =====")
    except subprocess.CalledProcessError as e:
        print(f"【エラー発生】daily_report.py実行失敗：{e}")

def main():
    # 仮想取引シミュレーション（複数回）
    schedule.every().day.at("09:00").do(run_main_script)
    schedule.every().day.at("12:00").do(run_main_script)
    schedule.every().day.at("18:00").do(run_main_script)

    # 日次まとめレポート送信（夜22:00）
    schedule.every().day.at("22:00").do(run_daily_report)

    print("===== スケジューラー起動中（09:00/12:00/18:00/22:00） =====")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
