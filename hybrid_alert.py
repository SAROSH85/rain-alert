import logging
import requests
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import LAT, LON, OPENWEATHER_API_KEY, RADAR_IMAGE_URL
from fetch_radar import analyze_radar_zones  # New logic

# Threshold to trigger rain alert in mm
RAIN_THRESHOLD = 3

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

    if mock:
        logging.info("🧪 MOCK mode active")
        rain_data = [("Hour 1", 10), ("Hour 2", 20), ("Hour 3", 30)]
        chart_path = generate_rainfall_chart(rain_data, "mock_chart.png")
        alert_message = "🌧 Mock Rain Alert: Heavy rain expected. Stay safe!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Mock Rain Alert", alert_message, chart_path)
        return {"result": "✅ Mock alert sent"}

    # --- Step 1: Check forecast rain from OpenWeather ---
    rain_forecast = fetch_openweather_rain()
    alert_triggered = rain_forecast > RAIN_THRESHOLD

    # --- Step 2: AI Radar Image Analysis by Zone ---
    zone_summary, dark_zones = analyze_radar_zones()
    formatted_zone_text = "\n".join([f"📍 {z}: {emoji}" for z, emoji in zone_summary.items()])

    # --- Step 3: If rain, generate chart and send alert ---
    if alert_triggered or dark_zones:
        chart_path = generate_rainfall_chart([("Forecast", rain_forecast)], "live_chart.png")
        alert_msg = f"🌧 Rain Alert: {rain_forecast} mm forecasted.\n\n{formatted_zone_text}"
        send_telegram_alert(alert_msg, chart_path)
        send_email_alert("🌧 Rain Alert", alert_msg, chart_path)
        return {"result": "🚨 Rain alert sent", "zones": zone_summary}

    # --- Step 4: No rain, but still send summary with zones ---
    no_rain_msg = f"☀️ No rain alerts or forecast available currently.\n\n{formatted_zone_text}"
    send_telegram_alert(no_rain_msg)
    send_email_alert("☀️ No Rain Alert", no_rain_msg)
    return {"result": "☀️ No rain", "zones": zone_summary}