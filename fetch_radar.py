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

def detect_rainfall_for_zone(image, coords):
    """Simple placeholder logic to detect rainfall in mm from radar pixels."""
    try:
        x1, y1, x2, y2 = coords
        zone_crop = image.crop((x1, y1, x2, y2))
        zone_array = np.array(zone_crop)

        # Example: detect brightness → rainfall estimation
        avg_intensity = np.mean(zone_array)
        rainfall_mm = round((avg_intensity / 255) * 10, 1)  # scale 0–10 mm
        return rainfall_mm
    except Exception as e:
        logging.error(f"Rainfall detection failed for zone: {e}")
        return 0.0

def analyze_radar_zones(lat=None, lon=None):
    """
    Fetch radar image, analyze each zone, and return dict of rain status & mm.
    lat/lon args are accepted for compatibility but ignored (zones are fixed).
    """
    zones_result = {zone: {"status": "unknown", "mm": 0.0} for zone in ZONES}

    try:
        # Download radar image
        resp = requests.get(RADAR_IMAGE_URL, timeout=10)
        resp.raise_for_status()
        radar_img = Image.open(BytesIO(resp.content)).convert("RGB")

        for zone, coords in ZONES.items():
            rainfall_mm = detect_rainfall_for_zone(radar_img, coords)
            zones_result[zone]["mm"] = rainfall_mm

            if rainfall_mm >= 1:
                zones_result[zone]["status"] = "rain"
            elif 0 < rainfall_mm < 1:
                zones_result[zone]["status"] = "cloud"
            else:
                zones_result[zone]["status"] = "clear"

        return zones_result

    except Exception as e:
        logging.error(f"Failed to analyze radar zones: {e}")
        return {zone: {"status": "unknown", "mm": 0.0} for zone in ZONES}