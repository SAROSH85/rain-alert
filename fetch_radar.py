import logging
import numpy as np
import requests
from PIL import Image
from io import BytesIO

# Updated IMD radar image for Surface Rainfall Intensity
RADAR_IMAGE_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"

# Define Mumbai zones with (x1, y1, x2, y2) bounding boxes
ZONES = {
    "Colaba": (180, 270, 200, 290),
    "CST": (185, 260, 205, 280),
    "Fort": (180, 255, 200, 275),
    "Marine Lines": (175, 250, 195, 270),
    "Grant Road": (170, 245, 190, 265),
    "Lamington Road": (168, 242, 188, 262),
    "Mazgaon": (165, 240, 185, 260),
    "Byculla": (162, 238, 182, 258),
    "Lalbaug": (160, 235, 180, 255),
    "Parel": (158, 232, 178, 252),
    "Dadar": (155, 230, 175, 250),
    "Sion": (150, 225, 170, 245),
    "Kurla": (148, 220, 168, 240),
    "Ghatkopar": (145, 215, 165, 235),
    "Vikhroli": (140, 210, 160, 230),
    "Thane": (135, 205, 155, 225),
    "Powai": (130, 200, 150, 220),
    "Vashi": (125, 195, 145, 215),
}

def analyze_radar_zones():
    try:
        response = requests.get(RADAR_IMAGE_URL, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("L")  # Convert to grayscale
        img_array = np.array(img)

        zone_status = {}
        for zone, (x1, y1, x2, y2) in ZONES.items():
            region = img_array[y1:y2, x1:x2]
            avg_intensity = np.mean(region)

            if avg_intensity > 180:
                zone_status[zone] = "rain"
            elif avg_intensity > 100:
                zone_status[zone] = "cloud"
            else:
                zone_status[zone] = "clear"

        return zone_status

    except Exception as e:
        logging.error(f"Failed to analyze radar zones: {e}")
        return {zone: "unknown" for zone in ZONES}