# weekly_report.py
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
from notifier import send_email

def generate_weekly_summary():
    now = datetime.now()
    start = now - timedelta(days=7)

    df = pd.read_csv("signal_log.csv", header=None, names=["timestamp", "symbol", "signal", "price", "strategy"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df_week = df[df["timestamp"] >= start]

    if df_week.empty:
        return None, "今週のシグナルはありません。"

    summary = {
        "期間": f"{start.date()} 〜 {now.date()}",
        "総シグナル数": len(df_week),
        "BUY数": len(df_week[df_week["signal"] == "buy"]),
        "SELL数": len(df_week[df_week["signal"] == "sell"]),
    }

    strategy_stats = df_week.groupby("strategy").agg({
        "signal": "count",
        "price": "mean"
    }).rename(columns={"signal": "件数", "price": "平均価格"}).reset_index()

    return df_week, summary, strategy_stats

def export_pdf(df_week, summary, strategy_stats, filepath="weekly_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 概要
    pdf.cell(200, 10, txt=f"📊 週次トレードレポート", ln=True)
    for k, v in summary.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="🧠 戦略ごとの集計", ln=True)
    for _, row in strategy_stats.iterrows():
        pdf.cell(200, 10, txt=f"{row['strategy']}: 件数={row['件数']} 平均価格={row['平均価格']:.2f}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="📜 シグナル一覧", ln=True)
    for _, row in df_week.iterrows():
        pdf.cell(200, 10, txt=f"{row['timestamp']} - {row['signal'].upper()} {row['symbol']} @ {row['price']} [{row['strategy']}]", ln=True)

    pdf.output(filepath)
    return filepath

if __name__ == "__main__":
    try:
        df_week, summary, strategy_stats = generate_weekly_summary()
        if df_week is None:
            send_email("📊 今週のレポート", "今週のシグナルはありません。")
        else:
            filepath = export_pdf(df_week, summary, strategy_stats)
            send_email("📊 週次シグナルレポート（PDF添付）", "今週のレポートを添付します。", attachments=[filepath])
    except Exception as e:
        send_email("📛 週次レポート生成エラー", str(e))
