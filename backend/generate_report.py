# generate_report.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from backend.fpdf import FPDF
import datetime
import matplotlib
import matplotlib.font_manager as fm


matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'


def load_and_prepare():
    df = pd.read_csv("trade_log.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.to_period("M")
    df["week"] = df["timestamp"].dt.isocalendar().week
    return df

def create_cumulative_plot(df):
    df_daily = df.groupby("date")["pnl"].sum().cumsum()
    plt.figure(figsize=(8, 4))
    plt.plot(df_daily.index, df_daily.values, marker='o', color='green')
    plt.title("累積損益グラフ")
    plt.xlabel("日付")
    plt.ylabel("累積損益 (円)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cumulative_pnl.png")
    plt.close()

def summarize(df, field_name):
    grouped = df.groupby(field_name)["pnl"].agg(["count", "sum", "mean"])
    grouped.rename(columns={"count": "取引回数", "sum": "合計損益", "mean": "平均損益"}, inplace=True)
    return grouped

def add_table_to_pdf(pdf, title, summary_df):
    pdf.set_font("Noto", '', 14)
    pdf.cell(200, 10, txt=title, ln=True, align='L')
    pdf.set_font("Noto", size=10)
    pdf.cell(200, 6, txt=summary_df.to_string(), ln=True)
    pdf.ln(4)

def generate_pdf_report():
    df = load_and_prepare()
    create_cumulative_plot(df)

    today = datetime.date.today()
    pdf = FPDF()
    pdf.add_page()

    # ✅ 日本語フォント登録
    font_path = "fonts/NotoSansJP-Regular.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("フォントファイルが見つかりません")

    pdf.add_font("Noto", "", font_path, uni=True)
    pdf.set_font("Noto", size=14)  # ← 必ずこのフォント名を使用！

    # PDFタイトル
    pdf.cell(200, 10, txt=f"取引成績レポート（{today} 時点）", ln=True, align='C')
    pdf.ln(10)

    # 以下すべての `.cell()` や `.multi_cell()` で set_font("Noto") を使っておくこと

    yearly = summarize(df, "year")
    monthly = summarize(df, "month")
    weekly = summarize(df, "week")
    daily = summarize(df, "date")

    add_table_to_pdf(pdf, "【年次レポート】", yearly)
    add_table_to_pdf(pdf, "【月次レポート】", monthly)
    add_table_to_pdf(pdf, "【週次レポート】", weekly)
    add_table_to_pdf(pdf, "【日次レポート】", daily)

    pdf.add_page()
    pdf.set_font("Noto", size=14)
    pdf.cell(200, 10, txt="累積損益グラフ", ln=True, align='C')
    pdf.image("cumulative_pnl.png", x=10, y=30, w=190)

    filename = f"report_{today}.pdf"
    pdf.output(filename)
    print(f"PDFレポートを生成しました: {filename}")

if __name__ == '__main__':
    generate_pdf_report()
