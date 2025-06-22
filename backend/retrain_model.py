# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE  # SMOTE導入
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

# 特徴量を定義（使用する全てのカラム名を正確に）
features = [
    'open', 'high', 'low', 'close', 'volume', 'rsi', 'ma', 'ma_50', 'ma_200',
    'macd', 'macd_signal', 'macd_histogram', 'bb_upper', 'bb_middle', 'bb_lower',
    'bollinger_band_width', 'volatility', 'ma_diff', 'ma_trend', 'price_change',
    'price_range', 'volatility_ratio', 'ma_slope', 'rsi_slope', 'return_5',
    'return_10', 'rsi_change', 'close_mean_3', 'bb_width', 'rsi_volatility_combo',
    'macd_diff', 'ma_ratio', 'rsi_macd_diff', 'vol_bb_ratio', 'rsi_squared', 'macd_abs'
]

# データ読み込み
df = pd.read_csv("training_data.csv")
df = df.dropna()
X = df[features]
y = df["target"]

# データ標準化（SMOTE前に行うと良い結果になりやすい）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# SMOTE 適用（クラス1合成）
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)
print(f"✅ SMOTE適用後のクラス分布: {np.bincount(y_resampled)}")

# 学習用・検証用に分割
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# モデル定義（アンサンブル VotingClassifier）
xgb_clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss', scale_pos_weight=1.0, random_state=42)
lgb_clf = LGBMClassifier(random_state=42)
rf_clf = RandomForestClassifier(random_state=42)

ensemble_clf = VotingClassifier(
    estimators=[('xgb', xgb_clf), ('lgb', lgb_clf), ('rf', rf_clf)],
    voting='soft'
)

# モデル学習
ensemble_clf.fit(X_train, y_train)

# 予測（確率）
y_pred_proba = ensemble_clf.predict_proba(X_test)[:, 1]

# 最適なしきい値を探索（0.05〜0.50）
best_threshold = 0.5
best_f1 = 0
for th in np.arange(0.05, 0.50, 0.01):
    y_pred = (y_pred_proba > th).astype(int)
    report = classification_report(y_test, y_pred, output_dict=True)
    if report['1']['f1-score'] > best_f1:
        best_f1 = report['1']['f1-score']
        best_threshold = th

print(f"✅ 最適しきい値: {best_threshold:.2f}")

# 最終評価
y_pred_final = (y_pred_proba > best_threshold).astype(int)
print("✅ モデル再学習完了（SMOTE適用）")
print(f"正解率: {accuracy_score(y_test, y_pred_final):.4f}")
print("混同行列:")
print(confusion_matrix(y_test, y_pred_final))
print("📄 分類レポート:")
print(classification_report(y_test, y_pred_final))

import joblib

# 学習済みモデルの保存
joblib.dump(model, 'trained_model.pkl')
print("✅ モデルを 'trained_model.pkl' に保存しました。")

