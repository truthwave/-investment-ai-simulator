# plot_training_log.py

import pandas as pd
import matplotlib.pyplot as plt
import os

# ログファイルのパス
log_path = "training_log.csv"

# 文字コードを順に試して読み込み
encodings = ["utf-8", "cp932", "shift_jis", "latin1"]
df = None

for enc in encodings:
    try:
        df = pd.read_csv(log_path, parse_dates=["datetime"], encoding=enc)
        print(f"✅ 読み込み成功: encoding='{enc}'")
        break
    except Exception as e:
        print(f"⚠️ 読み込み失敗: encoding='{enc}' → {e}")

# 読み込みできなかった場合は終了
if df is None:
    print("❌ CSVファイルの読み込みに失敗しました。文字コードを確認してください。")
    exit()

# datetime列をインデックスに設定
df.set_index("datetime", inplace=True)

# グラフ描画（例：accuracy と recall_1 をプロット）
plt.figure(figsize=(10, 6))
plt.plot(df.index, df["accuracy"], marker="o", label="Accuracy", color="blue")
if "recall_1" in df.columns:
    plt.plot(df.index, df["recall_1"], marker="x", label="Recall (Class 1)", color="green")

plt.xlabel("DateTime")
plt.ylabel("Score")
plt.title("モデル精度の推移")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)

# 画像として保存も可能
plt.savefig("training_log_plot.png")
plt.show()
