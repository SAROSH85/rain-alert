import smtplib
import ssl
from email.message import EmailMessage
import os
import requests

from config import EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD


def send_email_alert(subject, message, image_paths=None):
    """
    Send email with optional multiple image attachments.
    """
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # Handle single or multiple images
        if image_paths:
            if isinstance(image_paths, str):
                image_paths = [image_paths]
            for idx, path in enumerate(image_paths, start=1):
                if path and os.path.exists(path):
                    with open(path, "rb") as f:
                        img_data = f.read()
                    filename = os.path.basename(path) or f"chart_{idx}.png"
                    msg.add_attachment(
                        img_data,
                        maintype="image",
                        subtype="png",
                        filename=filename,
                    )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email error:", e)


def send_telegram_alert(message, image_paths=None):
    """
    Send Telegram message with optional multiple images.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    # Always send text first
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    resp = requests.post(url, json=payload)
    print("Telegram message:", resp.status_code, resp.text)

    # If images exist, send them
    if image_paths:
        if isinstance(image_paths, str):
            image_paths = [image_paths]
        for path in image_paths:
            if path and os.path.exists(path):
                photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
                with open(path, "rb") as photo:
                    files = {"photo": photo}
                    data = {"chat_id": chat_id}
                    resp = requests.post(photo_url, data=data, files=files)
                    print("Telegram image:", resp.status_code, resp.text)