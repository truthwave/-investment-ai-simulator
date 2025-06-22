class TradingControl:
    def __init__(self):
        self.is_running = True

    def stop_trading(self):
        self.is_running = False
        return "AI自動売買を停止しました。"

    def start_trading(self):
        self.is_running = True
        return "AI自動売買を再開しました。"
