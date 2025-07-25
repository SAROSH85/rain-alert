import smtplib
import os
import requests
from email.mime.text import MIMEText
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, EMAIL_SENDER, EMAIL_RECEIVER

def send_telegram_alert(message: str, chart_path: str = None):
    token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    send_url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Send text alert
    requests.post(send_url, data={"chat_id": chat_id, "text": message})

    # If chart is available, send chart image
    if chart_path and os.path.exists(chart_path):
        files = {'photo': open(chart_path, 'rb')}
        send_photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
        requests.post(send_photo_url, data={"chat_id": chat_id}, files=files)

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
