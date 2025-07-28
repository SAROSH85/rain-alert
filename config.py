import os

# --- Location ---
LAT = float(os.getenv("LAT", 19.0760))  # Mumbai
LON = float(os.getenv("LON", 72.8777))  # Mumbai

# --- API Keys ---
WINDY_API_KEY = os.getenv("9S9NyPXTCsB882Lbvjw1EH56EfwHQ9IQ")
ACCU_API_KEY = os.getenv("JSZBzteqfPETsbKZIfUWGaRdXFRNuWSV")

# --- Telegram Bot ---
TELEGRAM_BOT_TOKEN = os.getenv("8007450378:AAGXc-2Y1PbyWn-7yDbq_wIG3-WWrQ-DULY")
TELEGRAM_CHAT_ID = os.getenv("8001098705")

# --- Email ---
EMAIL_SENDER = os.getenv("saroshxolo@gmail.com")
EMAIL_RECEIVER = os.getenv("saroshxolo@gmail.com")
EMAIL_PASSWORD = os.getenv("uhugfnjanfmijzmh")

# --- IMD Data Sources ---
GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar/mumbai_latest.png"

if __name__ == "__main__":
    print("✅ Windy Key:", bool(WINDY_API_KEY))
    print("✅ AccuWeather Key:", bool(ACCU_API_KEY))
    print("🤖 Telegram Token:", bool(TELEGRAM_BOT_TOKEN))
    print("📩 Email Sender:", EMAIL_SENDER)
    