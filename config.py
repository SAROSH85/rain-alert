import os

# --- Location ---
LAT = float(os.getenv("LAT", 19.0760))  # Mumbai
LON = float(os.getenv("LON", 72.8777))  # Mumbai

# --- API Keys ---
WINDY_API_KEY = os.getenv("WINDY_API_KEY")  # ✅ This must match your Render env var name
ACCU_API_KEY = os.getenv("ACCU_API_KEY")

# --- Telegram Bot ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Email ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("uhskfnuuflrkshft")  # ✅ This must be your 16-char Gmail App Password

# --- IMD Data Sources ---
GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar/mumbai_latest.png"

if __name__ == "__main__":
    print("✅ Windy Key:", bool(WINDY_API_KEY))
    print("✅ AccuWeather Key:", bool(ACCU_API_KEY))
    print("🤖 Telegram Token:", bool(TELEGRAM_BOT_TOKEN))
    print("📩 Email Sender:", EMAIL_SENDER)