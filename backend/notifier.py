import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))  # SSLポート
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
NOTIFY_TO_ADDRESS = os.getenv("NOTIFY_TO_ADDRESS")

# ✅ 汎用メール送信関数（PDF添付対応）
def send_email(subject, body, attachments=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = NOTIFY_TO_ADDRESS
    msg["Date"] = formatdate()

    msg.attach(MIMEText(body))

    if attachments:
        for filepath in attachments:
            with open(filepath, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filepath)}")
                msg.attach(part)

    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("✅ メール送信成功")
    except Exception as e:
        print(f"📛 メール送信失敗: {e}")

# オプション：エントリー通知
def send_entry_signal(symbol, price):
    subject = f"[Entry] {symbol}"
    body = f"Entry signal for {symbol} at {price}円"
    send_email(subject, body)

# オプション：イグジット通知
def send_exit_signal(symbol, price):
    subject = f"[Exit] {symbol}"
    body = f"Exit signal for {symbol} at {price}円"
    send_email(subject, body)
