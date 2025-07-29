import logging
import requests
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import (
    LAT, LON,
    WINDY_API_KEY, ACCU_API_KEY,
    GFS_URL, RADAR_IMAGE_URL
)

def fetch_windy_forecast():
    try:
        url = "https://api.windy.com/api/point-forecast/v2"
        params = {
            "lat": LAT,
            "lon": LON,
            "model": "gfs",
            "parameters": ["precipitation"],
            "key": WINDY_API_KEY,
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("precipitation", [])
    except Exception as e:
        logging.error(f"❌ Windy API error: {e}")
        return []

def fetch_accuweather_forecast():
    try:
        url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/204842?apikey={ACCU_API_KEY}&details=true&metric=true"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error(f"❌ AccuWeather API error: {e}")
        return []

def analyze_rain_data(mock: bool = False):
    logging.info("🔄 Starting rain analysis...")

    if mock:
        logging.info("🧪 MOCK mode: generating fake rain alert.")
        rain_data = [("Hour 1", 10), ("Hour 2", 20), ("Hour 3", 30)]
        chart_path = generate_rainfall_chart(rain_data, "mock_chart.png")
        alert_message = "🌧 Mock Rain Alert: Heavy rain expected. Stay safe!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Mock Rain Alert", alert_message, chart_path)
        return {"result": "✅ Mock alert sent"}

    # --- Real data ---
    windy_data = fetch_windy_forecast()
    accuweather_data = fetch_accuweather_forecast()

    # --- Debug print ---
    logging.info("🌐 Checking live rain data...")
    logging.info(f"🌧 Windy response: {windy_data}")
    logging.info(f"🌧 AccuWeather response: {accuweather_data}")

    rain_forecast = 0

    if windy_data and isinstance(windy_data, list):
        rain_forecast = max(rain_forecast, max(windy_data))

    if accuweather_data:
        acc_rain = max([h.get("Rain", {}).get("Value", 0) for h in accuweather_data])
        rain_forecast = max(rain_forecast, acc_rain)

    logging.info(f"☁️ Combined Rain Forecast: {rain_forecast} mm")

    # --- Threshold logic ---
    if rain_forecast > 5:
        chart_path = generate_rainfall_chart([("Forecast", rain_forecast)], "live_chart.png")
        alert_message = f"🌧 Rain Alert: {rain_forecast} mm predicted. Carry umbrellas!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Rain Alert", alert_message, chart_path)
        return {"result": "🚨 Rain alert triggered"}

    return {"result": "☀️ No rain alerts or forecast available currently."}