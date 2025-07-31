import logging
import requests
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import LAT, LON, OPENWEATHER_API_KEY, RADAR_IMAGE_URL

def fetch_openweather_rain():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": LAT,
            "lon": LON,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        rain_1h = data.get("rain", {}).get("1h", 0)
        logging.info(f"🌧 OpenWeather Rain 1h: {rain_1h} mm")
        return rain_1h
    except Exception as e:
        logging.error(f"❌ OpenWeather API error: {e}")
        return 0

def analyze_rain_data(mock: bool = False):
    logging.info("🔄 Starting rain analysis...")

    # --- MOCK MODE ---
    if mock:
        logging.info("🔄 MOCK mode: generating fake rain alert.")
        rain_data = [("Hour 1", 10), ("Hour 2", 20), ("Hour 3", 30)]
        chart_path = generate_rainfall_chart(rain_data, "mock_chart.png")
        alert_message = "🌧 Mock Rain Alert: Heavy rain expected. Stay safe!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Mock Rain Alert", alert_message, chart_path)
        return {"result": "✅ Mock alert sent"}

    # --- LIVE MODE ---
    rain_forecast = fetch_openweather_rain()

    if rain_forecast > 3:
        chart_path = generate_rainfall_chart([("Forecast", rain_forecast)], "live_chart.png")
        alert_message = f"🌧 Rain Alert: {rain_forecast} mm predicted. Carry umbrellas!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Rain Alert", alert_message, chart_path)
        return {"result": "🚨 Rain alert triggered"}

    # --- NO RAIN SUMMARY ---
    alert_message = "☀️ No rain alerts or forecast available currently."
    send_telegram_alert(alert_message)
    send_email_alert("☀️ No Rain Alert", alert_message)
    return {"result": alert_message}