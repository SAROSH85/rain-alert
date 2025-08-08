import logging
import requests
from datetime import datetime

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