import smtplib
import os
import requests
from email.mime.text import MIMEText
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, EMAIL_SENDER, EMAIL_RECEIVER

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print("Telegram error:", e)
        return False

def send_email_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_SENDER, os.getenv("EMAIL_PASSWORD"))
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        return True
    except Exception as e:
        print("Email error:", e)
        return False
