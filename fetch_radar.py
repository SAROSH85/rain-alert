import requests

RADAR_IMAGE_URL = "https://mausam.imd.gov.in/radar/mumbai_latest.png"

def fetch_radar_image(save_path="radar_latest.png"):
    try:
        response = requests.get(RADAR_IMAGE_URL)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        else:
            print(f"Failed to fetch radar image. Status: {response.status_code}")
            return None
    except Exception as e:
        print("Radar fetch error:", e)
        return None
