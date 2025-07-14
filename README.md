# Stock Price Simulation & Automated Investment Strategy App

## 📌 Overview
This Python-based app automatically determines optimal weekly investment strategies using AI and simulates stock trades for S&P 500 and Nikkei 225 constituents. It also sends email notifications for trade signals and delivers weekly investment performance reports. The stock symbol lists are automatically scraped and updated monthly from Wikipedia.

⚠️ Disclaimer: This app is intended for educational and technical demonstration purposes only. It does not provide financial or investment advice.

## ⚙️ Key Features
📈 Stock Price Simulation
AI determines weekly buy/sell conditions and runs investment simulations.

📧 Notification System
Sends email alerts when trade signals are triggered.

📝 Weekly Reporting
Delivers weekly performance reports via email.

🔄 Automated Stock List Updates
Automatically scrapes and updates S&P 500 and Nikkei 225 stock lists monthly.

💡 Strategy Optimization
Rebuilds and fine-tunes investment strategies every week using AI.

## 🛠 Tech Stack
Python 3.x

pandas, scikit-learn (data analysis & AI modeling)

yfinance (fetching stock market data)

BeautifulSoup4 (web scraping)

smtplib, email (email notifications & reports)

matplotlib (data visualization)

## 🚀 How to Run
```bash
コードをコピーする
git clone https://github.com/your-username/stock-simulation-app.git
cd stock-simulation-app
pip install -r requirements.txt
python main.py
⚠️ Notes:

This repository does not include actual trading data or sensitive information like API keys or personal email credentials.

This project does not recommend specific investments or trading decisions.

✅ Skills Demonstrated
AI-driven financial modeling

Web scraping & data automation

Email notification systems

Data visualization and reporting

Python development
```



# 株価シミュレーション & 自動投資戦略アプリ

## 📌 概要
このアプリは、S&P500および日経平均の構成銘柄を対象に、AIが週ごとに最適な投資戦略を自動で決定し、株価をシミュレーションします。売買タイミングでのメール通知や週次の投資結果レポート送信を行います。銘柄リストは月1回、Wikipediaから自動で取得・更新します。

⚠️ 投資助言を目的としたものではありません。個人学習・技術デモ用途です。

---

## ⚙️ 主な機能
- 📈 **株価シミュレーション**：週次で売買条件をAIが決定し、シミュレーション実行
- 📧 **通知機能**：売買の局面でメール通知
- 📝 **レポート作成**：週次で投資結果のレポートをメール送信
- 🔄 **銘柄リスト自動更新**：S&P500・日経平均銘柄を月1でWebスクレイピングにより更新
- 💡 **戦略再構築**：AIが週次で投資戦略（売買条件）を最適化

---

## 🛠 技術スタック
- Python 3.x
- pandas / scikit-learn（データ分析・AI）
- yfinance（株価データ取得）
- BeautifulSoup4（Webスクレイピング）
- smtplib / email（通知・レポート送信）
- matplotlib（グラフ描画）

---

## 🚀 実行方法
```bash
git clone https://github.com/your-username/stock-simulation-app.git
cd stock-simulation-app
pip install -r requirements.txt
python main.py

⚠️ 注意事項
実データは含めておらず、APIキーや個人メールアドレス情報は除外しています。

投資判断や売買を推奨するものではありません。
