import tkinter as tk
from tkinter import ttk
from trading_manager import TradingManager
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Trading System")
        self.manager = TradingManager()

        # 価格表示
        self.price_label = tk.Label(root, text="現在の価格: 0", font=("Arial", 16))
        self.price_label.pack()

        # 収益表示
        self.profit_label = tk.Label(root, text="収益: 0", font=("Arial", 16))
        self.profit_label.pack()

        # 手動売買ボタン
        self.buy_button = tk.Button(root, text="BUY", command=self.manual_buy, bg="green", fg="white")
        self.buy_button.pack(side=tk.LEFT, padx=10)

        self.sell_button = tk.Button(root, text="SELL", command=self.manual_sell, bg="red", fg="white")
        self.sell_button.pack(side=tk.LEFT, padx=10)

        # 取引履歴テーブル
        self.tree = ttk.Treeview(root, columns=("Type", "Price", "Profit"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Profit", text="Profit")
        self.tree.pack()

        # グラフエリア
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # データ更新スレッド
        self.running = True
        threading.Thread(target=self.update_data, daemon=True).start()

    def manual_buy(self):
        self.manager.execute_trade("buy")

    def manual_sell(self):
        self.manager.execute_trade("sell")

    def update_data(self):
        while self.running:
            price = self.manager.get_price()
            profit = self.manager.total_profit

            # ラベル更新
            self.price_label.config(text=f"現在の価格: {price}")
            self.profit_label.config(text=f"収益: {profit}")

            # 取引履歴更新
            self.tree.delete(*self.tree.get_children())
            for trade in self.manager.trade_history:
                self.tree.insert("", "end", values=(trade["type"], trade["price"], trade["profit"]))

            # グラフ更新
            self.ax.clear()
            prices = [t["price"] for t in self.manager.trade_history]
            self.ax.plot(prices, label="Price")
            self.ax.legend()
            self.canvas.draw()

            time.sleep(1)

    def close(self):
        self.running = False
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
