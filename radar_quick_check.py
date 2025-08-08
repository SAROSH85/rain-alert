import logging
import requests
from datetime import datetime
from fetch_radar import analyze_radar_zones
from notify import send_telegram_alert, send_email_alert

# Official IMD Radar (Surface Rainfall Intensity)
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"

def check_radar_image_availability():
    try:
        response = requests.get(RADAR_IMAGE_URL, timeout=10)
        response.raise_for_status()
        logging.info("✅ IMD radar image available.")
        return True
    except Exception as e:
        logging.error(f"❌ Radar check failed: {e}")
        return False

def quick_radar_check():
    logging.basicConfig(level=logging.INFO)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    available = check_radar_image_availability()
    result = {
        "time": now,
        "radar_available": available
    }
    print(result)
    return result
    
    Checks for rain ≥ 1 mm in any Mumbai zone.
    Sends Telegram + Email alerts if detected.
    """
    logging.info("🚀 Running Quick Radar Rain Check...")

    radar_data = analyze_radar_zones()
    rain_zones = [zone for zone, status in radar_data.items() if status == "rain"]

    if rain_zones:
        message = "🌧 Quick Rain Alert: Rain ≥ 1 mm detected in:\n" + "\n".join([f"📍 {zone}" for zone in rain_zones])
        logging.info(message)

        # Send alerts
        send_telegram_alert(message)
        send_email_alert("🌧 Quick Rain Alert", message)

        return {"triggered": True, "zones": rain_zones}
    else:
        logging.info("✅ No rain ≥ 1 mm detected in any zone.")
        return {"triggered": False, "zones": []}

if __name__ == "__main__":
    quick_radar_check()
    
# radar_quick_check.py

from fetch_radar import analyze_radar_zones

def radar_check():
    zones = analyze_radar_zones()
    zone_messages = []

    for zone, status in zones.items():
        if status == "rain":
            zone_messages.append(f"📍 {zone}: 🌧️ Rain detected")
        elif status == "cloud":
            zone_messages.append(f"📍 {zone}: ☁️ Overcast")
        elif status == "clear":
            zone_messages.append(f"📍 {zone}: ☀️ Clear")
        else:
            zone_messages.append(f"📍 {zone}: ❓ Unknown")

    full_message = "🕒 Quick Radar Check (Every 10 mins)\n" + "\n".join(zone_messages)
    return {"message": full_message, "zones": zones}