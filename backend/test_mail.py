# test_mail.py
from notifier import send_email

send_email("✅ メール送信テスト", "これはテストメッセージです。\n通知が正しく届いていればOKです。")
