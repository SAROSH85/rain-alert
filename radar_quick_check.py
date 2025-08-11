import os
import requests
from io import BytesIO
from PIL import Image
from fetch_radar import ZONES  # Reuse your exact zone list
from notify import send_telegram_alert, send_email_alert

# IMD radar sources
SRI_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"  # Surface Rainfall Intensity
PAC_URL = "https://mausam.imd.gov.in/Radar/pac_vrv.gif"  # Precipitation Accumulation

RAIN_THRESHOLD = 1.0  # mm

def download_radar_image(url):
    """Download radar image from the given URL."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))

def analyze_radar_for_rain(image):
    """
    Analyze radar image and return zones where rain >= threshold.
    This assumes pixel intensity correlates with mm/h rainfall.
    """
    detected_zones = []
    for zone, (x1, y1, x2, y2) in ZONES.items():
        crop = image.crop((x1, y1, x2, y2)).convert("L")  # grayscale
        avg_pixel = sum(crop.getdata()) / (crop.width * crop.height)
        # Simple mapping: assume pixel intensity 255 = ~50 mm/h
        rainfall_mm = (avg_pixel / 255) * 50
        if rainfall_mm >= RAIN_THRESHOLD:
            detected_zones.append((zone, round(rainfall_mm, 1)))
    return detected_zones

def radar_quick_check():
    """Quick radar check for rain ≥ threshold."""
    try:
        sri_image = download_radar_image(SRI_URL)
    except Exception as e:
        return {"error": f"Failed to download radar image: {e}"}

    zones_with_rain = analyze_radar_for_rain(sri_image)

    if not zones_with_rain:
        return {"result": "No rain above threshold detected"}

    # Prepare alert text
    alert_lines = [f"🌧 Quick Rain Alert (≥ {RAIN_THRESHOLD} mm)"]
    for zone, rain in zones_with_rain:
        alert_lines.append(f"📍 {zone}: {rain} mm/h")
    alert_msg = "\n".join(alert_lines)

    # Send notifications
    try:
        send_telegram_alert(alert_msg)
    except Exception as e:
        print(f"❌ Telegram error: {e}")

    try:
        send_email_alert("Quick Rain Alert", alert_msg)
    except Exception as e:
        print(f"❌ Email error: {e}")

    return {"result": "✅ Quick alert sent", "zones": zones_with_rain}