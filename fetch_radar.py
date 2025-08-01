import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar_img/Mumbai_latest.png"

# Define Mumbai zones with (x1, y1, x2, y2) bounding boxes
ZONES = {
    "Colaba": (180, 270, 200, 290),
    "CST": (185, 260, 205, 280),
    "Dadar": (170, 240, 190, 260),
    "Powai": (150, 180, 170, 200),
    "Thane": (140, 160, 160, 180),
    "Vashi": (200, 220, 220, 240),
}

def fetch_and_process_radar_image():
    try:
        response = requests.get(RADAR_IMAGE_URL, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("L")  # grayscale
        return np.array(img)
    except Exception as e:
        print(f"❌ Failed to fetch radar image: {e}")
        return None

def analyze_radar_zones():
    img = fetch_and_process_radar_image()
    if img is None:
        return {zone: "⚠️ Image Error" for zone in ZONES}

    results = {}
    for zone, (x1, y1, x2, y2) in ZONES.items():
        zone_img = img[y1:y2, x1:x2]
        brightness = np.mean(zone_img)

        if brightness < 50:
            status = "🌧️ Rain detected"
        elif brightness < 100:
            status = "☁️ Overcast"
        else:
            status = "☀️ Clear"

        results[zone] = status

    return results