# train_model.py

from sklearn.metrics import f1_score
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
# パート３：モデルの定義と学習

# モデルを定義
from sklearn.ensemble import VotingClassifier
import xgboost as xgb
import lightgbm as lgb
from backend.catboost import CatBoostClassifier

# 各モデルのインスタンス
xgb_model = xgb.XGBClassifier(
    n_estimators=100, max_depth=5, learning_rate=0.1,
    scale_pos_weight=1.0, use_label_encoder=False, eval_metric='logloss'
)

lgbm_model = lgb.LGBMClassifier(
    n_estimators=100, max_depth=5, learning_rate=0.1,
    class_weight='balanced'
)

cat_model = CatBoostClassifier(
    iterations=100, depth=5, learning_rate=0.1,
    verbose=0, class_weights=[1.0, 3.0]
)

# アンサンブルモデルを構築
model = VotingClassifier(
    estimators=[
        ('xgb', xgb_model),
        ('lgbm', lgbm_model),
        ('cat', cat_model)
    ],
    voting='soft'
)

# 学習
model.fit(X_train, y_train)

ensemble_clf = VotingClassifier(
    estimators=[('xgb', xgb_clf), ('lgb', lgb_clf), ('rf', rf_clf)],
    voting='soft'
)

# モデル学習
ensemble_clf.fit(X_train, y_train)


# 予測確率
y_pred_proba = model.predict(X_test)

# 最適なしきい値を探索
thresholds = np.arange(0.1, 0.9, 0.01)
f1_scores = []

for t in thresholds:
    preds = (y_pred_proba >= t).astype(int)
    f1 = f1_score(y_test, preds, average="macro")
    f1_scores.append(f1)

best_threshold = thresholds[np.argmax(f1_scores)]

# パート: 高リスク予測の除外（confidence margin に基づくフィルタ）
confidence_margin = 0.1  # ここを調整可能（例：0.05～0.3くらい）
threshold = best_threshold

y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = (y_pred_proba >= threshold).astype(int)

# 中央0.5からmarginを外れた「高自信度」だけを評価対象にする
confidence_mask = (y_pred_proba < (0.5 - confidence_margin)) | (y_pred_proba > (0.5 + confidence_margin))
y_pred_confident = y_pred[confidence_mask]
y_test_confident = y_test[confidence_mask]

# 自信のある予測だけ抽出
X_eval = X_test[confidence_mask]
y_eval = y_test[confidence_mask]

# フィルター後の混同行列とレポート
print("✅ 高信頼予測のみの評価（confidence margin =", confidence_margin, "）")
print("評価対象サンプル数:", len(y_test_confident))
print(confusion_matrix(y_test_confident, y_pred_confident))
print(classification_report(y_test_confident, y_pred_confident))

# 最適なしきい値（例: 0.3） ※ GridSearch後に自動で決まるようにしている場合はそれを使う
optimal_threshold = 0.3
confidence_margin = 0.1  # 自信度のしきい値幅（例: ±10%）

# 最適な confidence_margin を探す
best_margin = None
best_f1 = 0
best_report = ""
best_confusion = None

print("📊 confidence_margin 最適化開始...")
for margin in np.arange(0.05, 0.35, 0.01):  # 0.05〜0.3 を 0.01 刻みで評価
    filtered_preds = []
    for p in y_pred_proba:
        if p >= optimal_threshold + margin:
            filtered_preds.append(1)
        elif p <= optimal_threshold - margin:
            filtered_preds.append(0)
        else:
            filtered_preds.append(-1)

    mask = np.array(filtered_preds) != -1
    y_eval = y_test[mask]
    y_pred_eval = np.array(filtered_preds)[mask]

    if len(y_eval) == 0:
        continue  # 予測なし

    f1 = f1_score(y_eval, y_pred_eval, average="macro")  # macro: クラス不均衡に対応
    if f1 > best_f1:
        best_f1 = f1
        best_margin = margin
        best_report = classification_report(y_eval, y_pred_eval)
        best_confusion = confusion_matrix(y_eval, y_pred_eval)

# 結果出力
print(f"✅ 最適 confidence_margin: {best_margin}")
print(f"✅ 最大 Macro F1-score: {round(best_f1, 4)}")
print("混同行列:")
print(best_confusion)
print("📄 分類レポート:")
print(best_report)

# 自信がある予測だけ通す（それ以外は -1 にする＝中立）
y_pred_filtered = []
for proba in y_pred_proba:
    if proba >= optimal_threshold + confidence_margin:
        y_pred_filtered.append(1)  # 強い買い予測
    elif proba <= optimal_threshold - confidence_margin:
        y_pred_filtered.append(0)  # 強い売り予測
    else:
        y_pred_filtered.append(-1)  # 自信ない → 中立扱い

# 中立(-1) を除外したデータだけで評価
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 有効な予測だけ取り出し
mask = np.array(y_pred_filtered) != -1
y_eval = y_test[mask]
y_pred_final = np.array(y_pred_filtered)[mask]

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

# パートN：学習結果のログ保存
import os
import csv
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, accuracy_score

# 評価指標を計算（必要に応じて再計算）
acc_score = accuracy_score(y_test, y_pred)
precision_1 = precision_score(y_test, y_pred, pos_label=1)
recall_0 = recall_score(y_test, y_pred, pos_label=0)

if os.path.exists("training_log.csv"):
    os.remove("training_log.csv")
    print("🧹 training_log.csv を削除しました。")

# ログファイルのパス
log_path = "training_log.csv"

from sklearn.metrics import accuracy_score

# ---- フィルタ対象の信頼度マスクを作成 ----
confidence_mask = (y_pred_proba >= 0.5 + best_margin) | (y_pred_proba <= 0.5 - best_margin)

# ---- フィルタ後の予測・正解ラベルを抽出 ----
y_pred_filtered = y_pred[confidence_mask]
y_test_filtered = y_test[confidence_mask]

# 予測と正解ラベルから accuracy を計算
accuracy = accuracy_score(y_test_filtered, y_pred_filtered)

macro_f1 = report["macro avg"]["f1-score"]

log_df = pd.DataFrame([{
    "datetime": pd.Timestamp.now(),
    "accuracy": accuracy,
    "macro_f1": macro_f1,
    "confidence_margin": best_margin
}])

log_df.to_csv(
    log_path,
    mode='a',
    index=False,
    header=not os.path.exists(log_path) 
)
# ヘッダーと現在のデータ行
log_fields = ["datetime", "accuracy", "precision_1", "recall_0"]
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
new_row = [now, acc_score, precision_1, recall_0]

# 書き込み処理（追記モード）
file_exists = os.path.isfile(log_path)
with open(log_path, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(log_fields)
    writer.writerow(new_row)

print(f"📝 ログを保存しました: {log_path}")

# パート6：精度比較と保存処理（モデル切り替え判定）
import os
import joblib

if os.path.exists("training_log.csv"):
    os.remove("training_log.csv")
    print("🧹 training_log.csv を削除しました。")

log_path = "training_log.csv"
old_model_path = "trained_model.pkl"
new_model_path = "trained_model_new.pkl"

# 最新の旧モデルスコアを取得
def get_last_f1_from_log(log_path):
    if not os.path.exists(log_path):
        return 0.0
    import pandas as pd
    df_log = pd.read_csv(log_path)
    if 'macro_f1' not in df_log.columns:
        return 0.0
    return df_log['macro_f1'].iloc[-1]

# confidence_margin 最適化後
threshold = best_threshold  # 最適しきい値を使う

# 高信頼度データだけに絞る（例：0.5 ± confidence_margin 以外）
confidence_mask = (y_pred_proba < (0.5 - confidence_margin)) | (y_pred_proba > (0.5 + confidence_margin))
X_eval = X_test[confidence_mask]
y_eval = y_test[confidence_mask]

# 絞ったデータで再度予測
y_pred_eval = (y_pred_proba[confidence_mask] >= best_threshold).astype(int)

# === confidence_margin 最適化 ===

# 信頼度マージンを用いた予測の信頼領域フィルタリング評価
from sklearn.metrics import classification_report

print("📊 confidence_margin 最適化開始...")

best_margin = 0.0
best_macro_f1 = 0.0
best_report = None
best_cm = None

for margin in np.arange(0.05, 0.5, 0.01):
    # 最終的な最適マージンでの予測結果を取得
    confidence_mask = (y_pred_proba < (0.5 - best_margin)) | (y_pred_proba > (0.5 + best_margin))
    best_y_pred_confident = y_pred[confidence_mask]
    best_y_test_confident = y_test.values[confidence_mask]

    # 評価レポートを再出力
    print("混同行列:")
    print(confusion_matrix(best_y_test_confident, best_y_pred_confident))
    print("📄 分類レポート:")
    print(classification_report(best_y_test_confident, best_y_pred_confident))

    # ログ保存（安全にキー確認）
    report = classification_report(best_y_test_confident, best_y_pred_confident, output_dict=True)
    precision_0 = report.get("0", {}).get("precision", 0.0)
    recall_0 = report.get("0", {}).get("recall", 0.0)
    f1_0 = report.get("0", {}).get("f1-score", 0.0)
    precision_1 = report.get("1", {}).get("precision", 0.0)
    recall_1 = report.get("1", {}).get("recall", 0.0)
    f1_1 = report.get("1", {}).get("f1-score", 0.0)


# 安全に各値を取得（キーが無い場合は0.0）
report = best_report or {}
precision_0 = report.get("0", {}).get("precision", 0.0)
recall_0 = report.get("0", {}).get("recall", 0.0)
f1_0 = report.get("0", {}).get("f1-score", 0.0)
precision_1 = report.get("1", {}).get("precision", 0.0)
recall_1 = report.get("1", {}).get("recall", 0.0)
f1_1 = report.get("1", {}).get("f1-score", 0.0)

# 自信度でフィルターされた予測と実際の正解ラベル
confidence_mask = (y_pred_proba < (0.5 - best_margin)) | (y_pred_proba > (0.5 + best_margin))
y_pred_filtered = y_pred[confidence_mask]
y_true_filtered = y_test.values[confidence_mask]

# 結果表示
print("混同行列:")
print(confusion_matrix(y_true_filtered, y_pred_filtered))
print("📄 分類レポート:")
print(classification_report(y_true_filtered, y_pred_filtered))


print(classification_report(y_true_filtered, y_pred_filtered))

# === confidence_margin の評価ログを保存 ===
log_file = "training_log.csv"
log_fields = [
    "datetime", "accuracy", "precision_0", "recall_0", "f1_0",
    "precision_1", "recall_1", "f1_1",
    "macro_f1", "confidence_margin", "n_confident"
]

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report = classification_report(best_y_test_confident, best_y_pred_confident, output_dict=True)

log_data = {
    "datetime": now,
    "accuracy": accuracy_score(best_y_test_confident, best_y_pred_confident),
    "precision_0": report["0"]["precision"],
    "recall_0": report["0"]["recall"],
    "f1_0": report["0"]["f1-score"],
    "precision_1": report["1"]["precision"],
    "recall_1": report["1"]["recall"],
    "f1_1": report["1"]["f1-score"],
    "macro_f1": best_f1,
    "confidence_margin": best_margin,
    "n_confident": len(best_y_test_confident),
}

# === CSVファイルに追記（ヘッダーがなければ追加） ===
file_exists = os.path.exists(log_file)
with open(log_file, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=log_fields)
    if not file_exists:
        writer.writeheader()
    writer.writerow(log_data)

print(f"📝 confidence_margin の結果ログを保存しました: {log_file}")

# 新旧比較して保存判断
macro_f1 = best_f1  # ← 修正：この行を上に移動して先に定義
last_macro_f1 = get_last_f1_from_log(log_path)
print(f"旧モデル Macro F1: {last_macro_f1:.4f} / 新モデル Macro F1: {macro_f1:.4f}")

if macro_f1 > last_macro_f1:
    joblib.dump(model, old_model_path)
    print("✅ 新モデルを保存しました（旧モデルより良好）")
else:
    print("⚠️ 旧モデルより精度が低いため保存しません")
