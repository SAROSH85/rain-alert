import logging
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import GFS_URL, RADAR_IMAGE_URL
import requests


def fetch_imd_gfs_forecast():
    try:
        r = requests.get(GFS_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("rainfall", [])  # Adjust key based on actual IMD JSON structure
    except Exception as e:
        logging.error(f"❌ IMD GFS API error: {e}")
        return []


def analyze_rain_data(mock: bool = False):
    logging.info("🔄 Starting rain analysis...")

    if mock:
        logging.info("🧪 MOCK mode enabled.")
        rain_data = [("Hour 1", 10), ("Hour 2", 20), ("Hour 3", 30)]
        chart_path = generate_rainfall_chart(rain_data, "mock_chart.png")
        alert_message = "🌧 Mock Rain Alert: Heavy rain expected. Stay safe!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Mock Rain Alert", alert_message, chart_path)
        return {"result": "✅ Mock alert sent"}

    # --- Real data from IMD GFS ---
    imd_data = fetch_imd_gfs_forecast()
    logging.info(f"📡 IMD GFS rainfall forecast: {imd_data}")

    rain_forecast = max(imd_data) if isinstance(imd_data, list) and imd_data else 0
    logging.info(f"🌧 Max rainfall forecast (IMD): {rain_forecast} mm")

    if rain_forecast > 5:
        chart_path = generate_rainfall_chart([("IMD Forecast", rain_forecast)], "live_chart.png")
        alert_message = f"🌧 Rain Alert: {rain_forecast} mm predicted. Carry umbrellas!"
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Rain Alert", alert_message, chart_path)
        return {"result": "🚨 Rain alert triggered"}

    return {"result": "☀️ No rain alerts or forecast available currently."}