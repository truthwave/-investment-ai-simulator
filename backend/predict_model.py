# パート1：必要ライブラリ読み込み
import pandas as pd
import numpy as np
import joblib
import random
from lightgbm import LGBMClassifier

# パート2：特徴量定義（訓練時と同じ順序で！）
features = [
    'open', 'high', 'low', 'close', 'volume',
    'rsi', 'ma', 'ma_50', 'ma_200',
    'macd', 'macd_signal', 'macd_histogram',
    'bb_upper', 'bb_middle', 'bb_lower',
    'bollinger_band_width', 'volatility',
    'ma_diff', 'ma_trend', 'price_change',
    'target', 'price_range', 'volatility_ratio',
    'ma_slope', 'rsi_slope', 'return_5', 'return_10',
    'rsi_change', 'close_mean_3', 'bb_width',
    'rsi_volatility_combo', 'macd_diff', 'ma_ratio',
    'rsi_macd_diff', 'vol_bb_ratio', 'rsi_squared', 'macd_abs'
]

# パート3：データ読み込み（最新の予測対象データ）
df = pd.read_csv("latest_data.csv")  # 最新データCSVがある前提
X = df[features]

# パート4：A/Bテストで使用するモデルを分岐
model_paths = {
    "A": "trained_model.pkl",        # 旧モデル
    "B": "trained_model_new.pkl"     # 新モデル（まだなければ同じものでもOK）
}

model_key = random.choice(["A", "B"])
model_path = model_paths[model_key]
model = joblib.load(model_path)

print(f"✅ 使用モデル: {model_key}（{model_path}）")

# パート5：予測処理
prob = model.predict_proba(X)[:, 1]
threshold = 0.5
pred = (prob > threshold).astype(int)

# パート6：自信度 margin による除外処理（任意）
confidence_margin = 0.05
confident = (prob > threshold + confidence_margin) | (prob < threshold - confidence_margin)

df["prediction"] = pred
df["confidence"] = prob
df["used_model"] = model_key
df["confident"] = confident

# パート7：結果保存
df.to_csv("prediction_result.csv", index=False)
print("✅ 予測結果を prediction_result.csv に保存しました")
