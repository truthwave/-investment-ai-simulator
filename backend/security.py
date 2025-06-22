import time

class SecurityManager:
    def __init__(self):
        self.last_request_time = 0
        self.request_count = 0
        self.max_requests_per_minute = 60  # 1分間に60リクエストまで

    def rate_limit_check(self):
        """APIリクエストのレートリミットを適用"""
        current_time = time.time()
        if current_time - self.last_request_time < 1:
            self.request_count += 1
        else:
            self.request_count = 1
            self.last_request_time = current_time

        if self.request_count > self.max_requests_per_minute:
            raise ValueError("リクエスト回数が多すぎます！")

    def enable_2fa(self, user_id):
        """2段階認証を適用（仮実装）"""
        print(f"ユーザー {user_id} に 2FAコードを送信しました。")
import time

class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.requests = []

    def is_request_allowed(self):
        now = time.time()
        self.requests = [req for req in self.requests if now - req < self.period]

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

import pyotp

SECRET_KEY = "JBSWY3DPEHPK3PXP"

def verify_2fa(user_code):
    """ユーザーの入力コードが正しいかチェック"""
    totp = pyotp.TOTP(SECRET_KEY)
    return totp.verify(user_code)
