import os

# API Configuration
API_KEY = os.getenv("API_KEY")  # For OpenWeather, Meteologix, etc.
LAT = float(os.getenv("LAT", 19.0760))  # Default: Mumbai
LON = float(os.getenv("LON", 72.8777))  # Default: Mumbai

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# IMD URLs
GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar/mumbai_latest.png"

# Debug print (optional)
if __name__ == "__main__":
    print("✅ API_KEY Set:", bool(API_KEY))
    print("📍 Coordinates:", LAT, LON)
    print("🤖 Telegram Token Set:", bool(TELEGRAM_BOT_TOKEN))
    print("📨 Email Config Set:", bool(EMAIL_SENDER and EMAIL_RECEIVER))
    print("🌧 GFS URL:", GFS_URL)
    print("🌩 Radar URL:", RADAR_IMAGE_URL)