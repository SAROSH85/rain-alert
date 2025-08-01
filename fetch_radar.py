import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

RADAR_IMAGE_URL = "https://mausam.imd.gov.in/imd_latest/contents/radar.jpg"

# Define coordinates for Mumbai zones (example)
ZONES = {
    "Colaba": (200, 310),
    "CST": (220, 300),
    "Dadar": (240, 290),
    "Kurla": (260, 280),
    "Powai": (280, 270),
    "Thane": (300, 260),
    "Vashi": (320, 250),
    "Borivali": (180, 320),
    "Andheri": (210, 305),
    "Grant Road": (230, 295),
    "Mazgaon": (225, 297),
    "Byculla": (227, 296),
    "Parel": (235, 292),
    "Sion": (250, 285),
    "Ghatkopar": (265, 278),
    "Vikhroli": (270, 275),
    "Marine Lines": (215, 299),
    "Fort": (218, 298),
    "Lalbaug": (233, 293)
}

def analyze_radar_zones():
    try:
        # Step 1: Download radar image
        response = requests.get(RADAR_IMAGE_URL, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("L")  # Convert to grayscale

        # Step 2: Convert to numpy array
        img_np = np.array(img)

        zone_results = {}
        rain_detected_zones = []

        for zone, (x, y) in ZONES.items():
            brightness = np.mean(img_np[y-2:y+2, x-2:x+2])  # 4x4 pixel average
            if brightness < 70:
                emoji = "🌧️ Rain detected"
                rain_detected_zones.append(zone)
            elif brightness < 120:
                emoji = "☁️ Overcast"
            else:
                emoji = "☀️ Clear"
            zone_results[zone] = emoji

        return zone_results, rain_detected_zones

    except Exception as e:
        print(f"Radar analysis error: {e}")
        return {}, []