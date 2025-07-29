import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_SENDER, EMAIL_RECEIVER, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests
import logging

def send_email(subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, os.environ["EMAIL_PASSWORD"])
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        logging.info("✅ Email sent successfully!")
    except Exception as e:
        logging.error(f"❌ Email error: {e}")

def send_telegram(message: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception(response.text)
        logging.info("✅ Telegram message sent!")
    except Exception as e:
        logging.error(f"❌ Telegram error: {e}")
