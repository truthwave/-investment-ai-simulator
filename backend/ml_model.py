# ml_model.py

from xgboost import XGBClassifier
import joblib

class MLTradeModel:
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            use_label_encoder=False,
            eval_metric="logloss"
        )

    def train(self, X, y):
        self.model.fit(X, y)
        joblib.dump(self.model, "ml_model.pkl")

    def predict(self, X):
        if isinstance(X, list):
            return self.model.predict([X])
        return self.model.predict(X)
