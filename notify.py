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

import requests
import os

def send_telegram_alert(message, image_path=None):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    # Send message
    resp = requests.post(url, json=payload)
    print("Telegram message:", resp.status_code, resp.text)

    # If image exists, send it
    if image_path and os.path.exists(image_path):
        photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
        with open(image_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": chat_id}
            resp = requests.post(photo_url, data=data, files=files)
            print("Telegram image:", resp.status_code, resp.text)