# Stock Price Simulation & Automated Investment Strategy App

> **“Experiment with AI-powered investing — without risking real money!”**

---

## 📌 Overview

This Python-based app simulates stock trading and automatically builds weekly investment strategies using AI.  
It targets the **S&P 500 and Nikkei 225 stocks**, helping users explore how AI might manage investments.  

Features include email notifications for buy/sell signals and weekly reports summarizing simulated portfolio results.  
**Stock lists update automatically each month** by scraping data from Wikipedia.

Ideal for:

- AI and finance enthusiasts
- Developers exploring financial modeling
- Students studying algorithmic trading
- Anyone curious about data-driven investment strategies

---

⚠️ **Disclaimer**  
- This app is for **educational and technical demonstration purposes only**.  
- It does **not** provide financial or investment advice.  
- Real trading decisions should be made at your own risk.

---

## ⚙️ Key Features

- 📈 **Stock Price Simulation**  
  Simulates weekly stock price movements using historical data and statistical methods.

- 🧠 **AI-Driven Strategy Updates**  
  Rebuilds and optimizes trading strategies every week, deciding when to buy, hold, or sell.

- 📧 **Notification System**  
  Sends email alerts when the AI triggers buy or sell signals.

- 📝 **Weekly Reporting**  
  Delivers performance summaries via email so users can track how virtual investments perform over time.

- 🔄 **Automated Stock List Updates**  
  Scrapes and updates S&P 500 and Nikkei 225 stock symbols from Wikipedia monthly.

- 💡 **Skill Development**  
  Great for practicing:
  - AI financial modeling
  - Data scraping and automation
  - Email notification systems
  - Data visualization and reporting

---

## 🛠 Tech Stack

- Python 3.x
- pandas, scikit-learn (data analysis & AI)
- yfinance (stock data fetching)
- BeautifulSoup4 (web scraping)
- smtplib, email (notifications & reports)
- matplotlib (data visualization)

---

## 🚀 How to Run

```bash
git clone https://github.com/your-username/stock-simulation-app.git
cd stock-simulation-app
pip install -r requirements.txt
python main.py
```

## 🔮 Future Plans
- Support for other markets beyond S&P 500 and Nikkei 225

- More advanced AI algorithms for strategy development

- Interactive dashboards for deeper analysis

- Cloud deployment for easier access

“Test your investment ideas safely — let AI show you what’s possible.”



# 株価シミュレーション & 自動投資戦略アプリ

## 📌 概要
このアプリは、S&P500および日経平均の構成銘柄を対象に、AIが週ごとに最適な投資戦略を自動で決定し、株価をシミュレーションします。
売買タイミングでのメール通知や、週次の投資結果レポート送信を行います。
銘柄リストは月1回、Wikipediaから自動で取得・更新します。

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

✅ このアプリで身につくスキル
AIによる金融モデリング

Webスクレイピングとデータ自動取得

メール通知システム構築

データ可視化とレポーティング

Python開発
