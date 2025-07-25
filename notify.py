import smtplib
import os
import requests
from email.mime.text import MIMEText
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, EMAIL_SENDER, EMAIL_RECEIVER

def send_telegram_alert(message: str, chart_path: str = None):
    """
    Sends a Telegram alert with optional image chart.
    """
    token = TELEGRAM_BOT_TOKEN  # fixed typo
    chat_id = TELEGRAM_CHAT_ID

    if chart_path and os.path.exists(chart_path):
        # Send photo with caption
        with open(chart_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id, 'caption': message, 'parse_mode': 'HTML'}
            requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data=data, files=files)
    else:
        # Send plain text message
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=data)

def send_email_alert(subject, body):
    """
    Sends an email using Gmail SMTP.
    """
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