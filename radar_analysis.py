
# radar_analysis.py

from PIL import Image
from radar_zones import MUMBAI_ZONES
import numpy as np

def classify_brightness(avg):
    if avg < 60:
        return "🌧️ Rain detected"
    elif avg < 120:
        return "☁️ Overcast"
    else:
        return "☀️ Clear"

def analyze_zones(image_path: str) -> dict:
    img = Image.open(image_path).convert("L")  # grayscale
    img_np = np.array(img)
    results = {}

    for zone, ((x1, y1), (x2, y2)) in MUMBAI_ZONES.items():
        cropped = img_np[y1:y2, x1:x2]
        avg_brightness = cropped.mean()
        results[zone] = classify_brightness(avg_brightness)

    return results
