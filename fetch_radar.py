import cv2
import numpy as np
import requests
from config import RADAR_IMAGE_URL
import logging
from io import BytesIO
from PIL import Image

RADAR_IMAGE_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"  # Surface Rainfall Intensity

# Use official IMD radar images
SRI_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"
PAC_URL = "https://mausam.imd.gov.in/Radar/pac_vrv.gif"
TEMP_FILE = "radar_image.gif"

# Define Mumbai zones with (x1, y1, x2, y2) bounding boxes
ZONES = {
    "Colaba": (180, 270, 200, 290),
    "CST": (185, 260, 205, 280),
    "Fort": (182, 255, 202, 275),
    "Marine Lines": (180, 250, 200, 270),
    "Grant Road": (175, 245, 195, 265),
    "Lamington Road": (174, 244, 194, 264),
    "Mazgaon": (178, 240, 198, 260),
    "Byculla": (172, 238, 192, 258),
    "Lalbaug": (170, 236, 190, 256),
    "Parel": (168, 234, 188, 254),
    "Dadar": (170, 230, 190, 250),
    "Sion": (160, 220, 180, 240),
    "Kurla": (158, 215, 178, 235),
    "Ghatkopar": (155, 210, 175, 230),
    "Vikhroli": (152, 205, 172, 225),
    "Thane": (140, 200, 160, 220),
    "Powai": (150, 195, 170, 215),
    "Vashi": (200, 210, 220, 230)
}

def download_radar_image(url=SRI_URL):
    try:
        response = requests.get(RADAR_IMAGE_URL, timeout=10)
        response.raise_for_status()
        with open(TEMP_FILE, "wb") as f:
            f.write(response.content)
        return TEMP_FILE
    except Exception as e:
        logging.error(f"Failed to download radar image: {e}")
        return None

def analyze_radar_zones():
    radar_img = download_radar_image()
    if not radar_path:
        return {zone: "unknown" for zone in ZONES}

    try:
        img = cv2.imread(radar_path, cv2.IMREAD_GRAYSCALE)
        zone_status = {}
        for zone, (x1, y1, x2, y2) in ZONES.items():
            region = img[y1:y2, x1:x2]
            avg_brightness = np.mean(region)
            if avg_brightness < 50:
                zone_status[zone] = "rain"
            elif avg_brightness < 100:
                zone_status[zone] = "cloud"
            else:
                zone_status[zone] = "clear"
        return zone_status
        
            for zone, (x1, y1, x2, y2) in ZONES.items():
            region = img_array[y1:y2, x1:x2]
            avg_intensity = np.mean(region)
            if avg_intensity > 180:
                zone_status[zone] = "rain"
            elif avg_intensity > 100:
                zone_status[zone] = "cloud"
            else:
                zone_status[zone] = "clear"
        return status
    except Exception as e:
        logging.error(f"Radar processing error: {e}")
        return {zone: "unknown" for zone in ZONES}

# Placeholder for public APIs like Zoom Earth or GPM Layer (to be used in future)
# def fetch_satellite_data():
#     ...