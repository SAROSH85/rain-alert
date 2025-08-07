import os

# --- Location ---
LAT = float(os.getenv("LAT", 19.0760))  # Mumbai
LON = float(os.getenv("LON", 72.8777))  # Mumbai

# --- API Keys ---
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --- Telegram Bot ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Email ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# --- IMD Data Sources ---
GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"

# --- Debug block ---
if __name__ == "__main__":
    print("🤖 Telegram Bot Token Present:", bool(TELEGRAM_BOT_TOKEN))
    print("📨 EMAIL_SENDER:", EMAIL_SENDER)
    print("📨 EMAIL_RECEIVER:", EMAIL_RECEIVER)
    print("🔐 EMAIL_PASSWORD Present:", bool(EMAIL_PASSWORD))
    print("🔐 EMAIL_PASSWORD Preview:", EMAIL_PASSWORD[:4] + "****" + EMAIL_PASSWORD[-2:] if EMAIL_PASSWORD else "❌ Not Set")