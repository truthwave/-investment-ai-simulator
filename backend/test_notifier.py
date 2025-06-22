from notifier import send_entry_signal

try:
    send_entry_signal("TEST_SYMBOL", 123.45)
except Exception as e:
    print(f"[送信エラー]: {e}")
