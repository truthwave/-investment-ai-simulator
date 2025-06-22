import socket

class Firewall:
    def __init__(self):
        self.allowed_ips = ["123.45.67.89"]  # 許可するIP

    def is_ip_allowed(self, ip):
        """許可されたIPアドレスかチェック"""
        return ip in self.allowed_ips

    def detect_anomalous_trade(self, trade_amount):
        """異常な取引額を検出（例: 10000USD以上は警告）"""
        if trade_amount > 10000:
            print("⚠️ 異常な取引が検出されました！")
            return True
        return False

import socket

ALLOWED_IPS = ["192.168.1.1", "203.0.113.42"]

def get_client_ip():
    return socket.gethostbyname(socket.gethostname())

def is_ip_allowed():
    client_ip = get_client_ip()
    return client_ip in ALLOWED_IPS
