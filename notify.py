import os
import smtplib
import requests
from email.message import EmailMessage
from config import (
    EMAIL_SENDER,
    EMAIL_RECEIVER,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)

def send_email_alert(subject: str, body: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, os.environ.get("EMAIL_PASSWORD"))
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email error: {e}")

def send_telegram_alert(message: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("✅ Telegram alert sent!")
    except Exception as e:
        print(f"❌ Telegram error: {e}")