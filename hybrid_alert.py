import requests
import logging
import os
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert
from config import GFS_URL, RADAR_IMAGE_URL

logging.basicConfig(level=logging.INFO)

def analyze_rain_data(mock: bool = False):
    if mock:
        logging.info("🔄 MOCK mode: Generating a fake rain alert.")
        alert_message = "🌧 Mock Rain Alert: Simulated heavy rainfall detected in Mumbai.\nTake precautions. Stay safe! 🚨"
        chart_path = generate_rainfall_chart([10, 20, 30], "mock_chart.png")
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("Mock Rain Alert", alert_message, chart_path)
        return alert_message

    logging.info("✅ Starting live rain analysis...")

    # --- 1. Fetch GFS Forecast Data ---
    try:
        gfs_response = requests.get(GFS_URL, timeout=10)
        gfs_response.raise_for_status()
        gfs_data = gfs_response.json()
        logging.info(f"📡 GFS Raw Data: {gfs_data}")
    except Exception as e:
        logging.error(f"❌ Error fetching GFS data: {e}")
        gfs_data = {}

    # --- 2. Fetch Radar Image ---
    radar_status_code = None
    try:
        radar_response = requests.get(RADAR_IMAGE_URL, timeout=10)
        radar_status_code = radar_response.status_code
        logging.info(f"📡 Radar Image Fetch Status: {radar_status_code}")
    except Exception as e:
        logging.error(f"❌ Error fetching radar image: {e}")

    # --- 3. Determine Rain Forecast ---
    rain_forecast = gfs_data.get("rain_forecast", 0)
    logging.info(f"🌧 Extracted rain_forecast value: {rain_forecast}")

    # Example threshold: rain_forecast > 5 means rain expected
    if isinstance(rain_forecast, (int, float)) and rain_forecast > 5:
        alert_message = f"🌧 Rain Alert: Heavy rain expected. IMD Radar status: {radar_status_code}"
        chart_path = generate_rainfall_chart([rain_forecast], "rain_chart.png")
        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Mumbai Rain Alert Update", alert_message, chart_path)
        logging.info("✅ Rain alert triggered and sent.")
        return alert_message
    else:
        logging.info("☀️ No rain alert triggered. Forecast too low or data missing.")
        return "☀️ No rain alerts or forecast available currently."