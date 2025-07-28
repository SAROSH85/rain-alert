import logging
import requests
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import LAT, LON, WINDY_API_KEY, ACCU_API_KEY

def get_windy_forecast(lat, lon):
    try:
        url = f"https://api.windy.com/api/point-forecast/v2?lat={lat}&lon={lon}&key={WINDY_API_KEY}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logging.error(f"Windy fetch error: {e}")
    return None

def get_accuweather_forecast(lat, lon):
    try:
        loc_url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={ACCU_API_KEY}&q={lat},{lon}"
        loc_resp = requests.get(loc_url, timeout=10)
        if loc_resp.status_code != 200:
            return None
        location_key = loc_resp.json().get("Key")

        forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}?apikey={ACCU_API_KEY}&details=true"
        forecast_resp = requests.get(forecast_url, timeout=10)
        if forecast_resp.status_code == 200:
            return forecast_resp.json()
    except Exception as e:
        logging.error(f"AccuWeather fetch error: {e}")
    return None

def analyze_rain_data(mock=False):
    logging.info("🔄 Starting rain analysis...")

    if mock:
        rain_data = [("Hour 1", 10), ("Hour 2", 20), ("Hour 3", 30)]
        chart_path = generate_rainfall_chart(rain_data, "mock_chart.png")
        msg = "🌧 Mock Rain Alert: Simulated heavy rainfall detected.\nStay safe!"
        send_telegram_alert(msg, chart_path)
        send_email_alert("🌧 Mock Rain Alert", msg, chart_path)
        return {"result": "✅ Mock alert sent"}

    windy_data = get_windy_forecast(LAT, LON)
    accuweather_data = get_accuweather_forecast(LAT, LON)

    windy_rain = windy_data.get("rain", {}).get("probability", 0) if windy_data else 0
    accu_rain = accuweather_data[0].get("PrecipitationProbability", 0) if accuweather_data else 0

    max_rain = max(windy_rain, accu_rain)
    logging.info(f"Windy rain: {windy_rain}%, Accu rain: {accu_rain}%")

    if max_rain > 60:
        rain_data = [("Next Hour", max_rain)]
        chart_path = generate_rainfall_chart(rain_data, "rain_alert.png")
        msg = f"🌧 Rain Alert: Probability {max_rain}%.\nTake precautions!"
        send_telegram_alert(msg, chart_path)
        send_email_alert("🌧 Rain Alert", msg, chart_path)
        return {"result": f"🚨 Rain alert triggered ({max_rain}%)"}

    return {"result": "☀️ No rain alerts or forecast available currently."}
