<p align="center">
<img width="996" height="670" alt="段落テキスト" src="https://github.com/user-attachments/assets/1f09bdca-b973-4f56-aa5d-38c62e811069" />

</p>

<h1 align="center">📊 株価シミュレーション × 自動投資戦略アプリ</h1>

<p align="center"><i>感情を排除した“合理的な投資判断”を、AIが自動で提案</i></p>

---

## 📌 概要

このアプリは、S&P500および日経平均の構成銘柄を対象に、  
**AIが毎週売買戦略を立案し、仮想売買と投資結果のレポートを完全自動で行うシミュレーター**です。

売買のタイミングをメールで通知し、運用成績を週次レポートで可視化。  
銘柄リストは月1回、Wikipediaから自動取得されるため、常に最新の構成銘柄で戦略が実行されます。

> ⚠️ このアプリは投資助言を目的としたものではなく、個人学習・技術デモ用ツールです。

---

## ⚙️ 主な機能

- 📈 **株価シミュレーション**  
　AIが売買戦略（ルール）を自動生成し、週次で仮想売買を実行

- 📧 **売買タイミング通知**  
　取引の局面で、自動的にメールでお知らせ

- 📝 **週次レポート送信**  
　損益・勝率などをまとめたレポートを、毎週自動で作成・送信

- 🔄 **銘柄リストの自動更新**  
　S&P500・日経平均の構成銘柄を、Wikipediaから月1でスクレイピング更新

- 💡 **戦略の定期再構築**  
　AIが週ごとに最適な戦略へアップデート

---

## 🛠 使用技術・ライブラリ

- Python 3.x
- `pandas`, `scikit-learn`：データ分析・AIモデル
- `yfinance`：株価データ取得
- `BeautifulSoup4`：Webスクレイピング
- `smtplib`, `email`：メール通知・レポート送信
- `matplotlib`：グラフ描画

---

## 📬 メール通知の例

売買タイミングになると、自動的にメールで通知されます：

<p align="center">
  <img src="https://github.com/user-attachments/assets/51277f69-2d4d-426f-a78e-ab2bcad8acfe" width="500" />
</p>

---

## 🚀 実行方法

```bash
git clone https://github.com/TomoProgrammingDayori/stock-simulation-app.git
cd stock-simulation-app
pip install -r requirements.txt
python main.py
````

> ⚠️ 注意：実データ・APIキー・個人メールアドレスなどは含まれていません。
> 設定が必要な箇所は、README内のコメントを参照してください。

---

## ✅ このアプリで身につくスキル

* AIによる投資戦略のモデリング
* Webスクレイピングとデータ自動更新
* Pythonによる通知・レポートの自動化
* データ可視化と週次レポーティング
* 実用的なAI × 金融の組み合わせ構築力

---

## 🧑‍💻 作者

**[ともプログラム便り](https://github.com/TomoProgrammingDayori)**
ポートフォリオやAIツール開発に関する情報も発信中です。ぜひご覧ください！
