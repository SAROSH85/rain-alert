import os

# External API or IMD Sources
GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar/mumbai_latest.png"

# Location
LAT = 19.0760
LON = 72.8777

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8007450378:AAGXc-2Y1PbyWn-7yDbq_wIG3-WWrQ-DULY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8001098705")

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "saroshxolo@gmail.com")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "saroshxolo@gmail.com")
