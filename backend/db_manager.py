import sqlite3
from cryptography.fernet import Fernet

# 鍵を生成（最初の1回のみ実行）
# key = Fernet.generate_key()
# print(f"データベース暗号化キー: {key}")

ENCRYPTION_KEY = b"ここに暗号化キーをセット"

class DatabaseManager:
    def __init__(self, db_path="trades.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.fernet = Fernet(ENCRYPTION_KEY)
        self.create_table()

    def create_table(self):
        """取引データのテーブルを作成"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_type TEXT,
            price REAL,
            profit REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()

    def save_trade(self, trade_type, price, profit):
        """取引データを暗号化して保存"""
        encrypted_price = self.fernet.encrypt(str(price).encode())
        encrypted_profit = self.fernet.encrypt(str(profit).encode())
        self.cursor.execute("INSERT INTO trades (trade_type, price, profit, timestamp) VALUES (?, ?, ?, datetime('now'))",
                            (trade_type, encrypted_price, encrypted_profit))
        self.conn.commit()

from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def save_trade(trade):
    encrypted_trade = encrypt_data(str(trade))
    with open("trades.db", "ab") as f:
        f.write(encrypted_trade + b"\n")
