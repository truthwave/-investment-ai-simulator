import joblib

# 保存されたモデルの読み込み
model = joblib.load('trained_model.pkl')
print("✅ モデルを読み込みました。")

# 予測データの読み込み
import pandas as pd
X_new = pd.read_csv("predict_data.csv")

# 予測
pred = model.predict(X_new)
print("予測結果:", pred)
