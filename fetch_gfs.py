import requests

GFS_URL = "https://mausam.imd.gov.in/api/gfs/mumbai.json"

def fetch_gfs_forecast():
    try:
        response = requests.get(GFS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print("GFS fetch failed:", response.status_code)
            return None
    except Exception as e:
        print("GFS fetch error:", e)
        return None
