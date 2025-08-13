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
    zones = {
        "Colaba": {"status": "clear", "mm": 0.0},
        "CST": {"status": "clear", "mm": 0.0},
        # ... rest of your current zone list
    }

    # Your existing radar analysis logic here...
    # Instead of only assigning "rain", also estimate mm
for zone in zones:
    try:
            
        rainfall_mm = detect_rainfall_for_zone(zone)  # Your radar logic
        if rainfall_mm >= 1:
            zones[zone]["status"] = "rain"
        elif 0 < rainfall_mm < 1:
            zones[zone]["status"] = "cloud"
        else:
            zones[zone]["status"] = "clear"
        zones[zone]["mm"] = round(rainfall_mm, 1)

    return zones

    except Exception as e:
        logging.error(f"Failed to analyze radar zones: {e}")
        return {zone: "unknown" for zone in ZONES}