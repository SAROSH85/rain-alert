import logging
import requests
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import LAT, LON, OPENWEATHER_API_KEY, GFS_URL, RADAR_IMAGE_URL


def fetch_openweather_forecast():
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        rain = data.get("rain", {})
        rain_1h = rain.get("1h", 0)
        rain_3h = rain.get("3h", 0)
        logging.info(f"☁️ OpenWeatherMap Rain 1h: {rain_1h} mm, Rain 3h: {rain_3h} mm")
        return max(rain_1h, rain_3h)
    except Exception as e:
        logging.error(f"❌ OpenWeatherMap API error: {e}")
        return 0


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

    # --- Real OpenWeatherMap Data ---
    rain_forecast = fetch_openweather_forecast()

    logging.info(f"🌧 Total Rain Forecast: {rain_forecast} mm")

    if rain_forecast > 5:
        chart_path = generate_rainfall_chart([("Forecast", rain_forecast)], "live_chart.png")
        alert_message = f"🌧 Rain Alert: {rain_forecast} mm predicted. Carry umbrellas!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Rain Alert", alert_message, chart_path)
        return {"result": "🚨 Rain alert triggered"}

    return {"result": "☀️ No rain alerts or forecast available currently."}