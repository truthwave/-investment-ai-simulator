# send_report.py

import smtplib
import datetime
import pandas as pd
from email.message import EmailMessage
from email.utils import formatdate
import os
from dotenv import load_dotenv

def summarize(df, field):
    summary = df.groupby(field)["pnl"].agg(["count", "sum", "mean"])
    summary["勝率"] = df[df["pnl"] > 0].groupby(field)["pnl"].count() / summary["count"]
    summary = summary.fillna(0)
    summary.columns = ["取引数", "合計損益", "平均損益", "勝率"]
    return summary.round(2)

def generate_summary_text():
    df = pd.read_csv("trade_log.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["week"] = df["timestamp"].dt.isocalendar().week
    df["month"] = df["timestamp"].dt.to_period("M")
    df["year"] = df["timestamp"].dt.year

    # 今週・今月・今年
    today = datetime.date.today()
    current_week = today.isocalendar()[1]
    current_month = today.strftime("%Y-%m")
    current_year = today.year

    week_summary = summarize(df[df["week"] == current_week], "week")
    month_summary = summarize(df[df["month"] == current_month], "month")
    year_summary = summarize(df[df["year"] == current_year], "year")

    text = f"""\
【今週の取引要約】
{week_summary.to_string()}

【今月の取引要約】
{month_summary.to_string()}

【今年の取引要約】
{year_summary.to_string()}
"""
    return text

def send_email_report():
    today = datetime.date.today()
    filename = f"report_{today}.pdf"
    filepath = f"./{filename}"
    summary_text = generate_summary_text()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    

    # .envファイル読み込み
    load_dotenv()

    # メール情報を環境変数から取得
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_TO")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Date"] = formatdate()
    msg["Subject"] = f"取引レポート（{today}）"
    msg.set_content(f"""\
お疲れ様です。

以下は自動生成されたトレード要約です。

{summary_text}

レポートPDFも添付しています。引き続き良いトレードを！

- 自動トレードAIシステムより
""")

    # 添付ファイル
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=filename)
    else:
        msg.set_content(msg.get_content() + "\n※PDFファイルが見つかりませんでした。")

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)

    print(f"✅ メール送信完了（{recipient} へ）")

if __name__ == "__main__":
    send_email_report()
