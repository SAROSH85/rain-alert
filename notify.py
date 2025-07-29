import smtplib
import ssl
from email.message import EmailMessage
import os

from config import EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD

def send_email_alert(subject, message, image_path=None):
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                img_data = f.read()
            msg.add_attachment(img_data, maintype="image", subtype="png", filename="chart.png")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email error:", e)

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