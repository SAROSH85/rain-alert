import smtplib
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, EMAIL_SENDER, EMAIL_RECEIVER

def send_telegram_alert(message: str, chart_path: str = None):
    token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    send_url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Send text alert
    requests.post(send_url, data={"chat_id": chat_id, "text": message})

    # If chart is available, send chart image
    if chart_path and os.path.exists(chart_path):
        with open(chart_path, 'rb') as photo:
            files = {'photo': photo}
            send_photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
            requests.post(send_photo_url, data={"chat_id": chat_id}, files=files)

def send_email_alert(subject: str, body: str, chart_path: str = None):
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # Add text content
        msg.attach(MIMEText(body, "plain"))

        # Attach chart image if available
        if chart_path and os.path.exists(chart_path):
            with open(chart_path, 'rb') as f:
                img_data = f.read()
                image = MIMEImage(img_data, name=os.path.basename(chart_path))
                msg.attach(image)

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_SENDER, os.getenv("EMAIL_PASSWORD"))
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        return True
    except Exception as e:
        print("Email error:", e)
        return False