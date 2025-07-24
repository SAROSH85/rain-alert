
import requests
from datetime import datetime
from config import API_KEY, LAT, LON

def check_rain_forecast():
    url = f"https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "metric",
        "exclude": "current,minutely,daily,alerts"
    }
    response = requests.get(url, params=params)
    data = response.json()

    rain_events = []
    for hour in data.get("hourly", [])[:6]:
        dt = datetime.fromtimestamp(hour['dt']).strftime('%I %p')
        rain = hour.get("rain", {}).get("1h", 0)
        if rain > 0:
            rain_events.append({
                "time": dt,
                "amount_mm": rain
            })

    return rain_events
