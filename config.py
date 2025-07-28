import os

WINDY_API_KEY = os.getenv("9S9NyPXTCsB882Lbvjw1EH56EfwHQ9IQ")
ACCU_API_KEY = os.getenv("JSZBzteqfPETsbKZIfUWGaRdXFRNuWSV")

LAT = float(os.getenv("LAT", 19.0760))
LON = float(os.getenv("LON", 72.8777))

TELEGRAM_BOT_TOKEN = os.getenv("8007450378:AAGXc-2Y1PbyWn-7yDbq_wIG3-WWrQ-DULY")
TELEGRAM_CHAT_ID = os.getenv("8001098705")

EMAIL_SENDER = os.getenv("saroshxolo@gmail.com")
EMAIL_RECEIVER = os.getenv("saroshxolo@gmail.com")
EMAIL_PASSWORD = os.getenv("uhugfnjanfmijzmh")

GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar/mumbai_latest.png"

if __name__ == "__main__":
    print("Windy key set:", bool(WINDY_API_KEY))
    print("Accu key set:", bool(ACCU_API_KEY))
    print("Telegram token:", bool(TELEGRAM_BOT_TOKEN))
    print("Email config:", bool(EMAIL_SENDER and EMAIL_PASSWORD))
