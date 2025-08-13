import logging
import requests
from charts import generate_rainfall_chart, generate_colored_bar_chart
from notify import send_telegram_alert, send_email_alert
from config import LAT, LON, OPENWEATHER_API_KEY
from fetch_radar import analyze_radar_zones, ZONES

def fetch_openweather_rain():
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
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
        rain_data = [("Hour 1", 0.5), ("Hour 2", 1.2), ("Hour 3", 2.0)]
        chart_line = generate_rainfall_chart(rain_data, "mock_line.png")
        chart_bar = generate_colored_bar_chart(rain_data, "mock_bar.png")
        alert_message = "🌧 Mock Rain Alert: Heavy rain expected. Stay safe!"
        send_telegram_alert(alert_message, [chart_line, chart_bar])
        send_email_alert("🌧 Mock Rain Alert", alert_message, [chart_line, chart_bar])
        return {"result": "✅ Mock alert sent"}

    # --- LIVE DATA FETCH ---
    rain_forecast = fetch_openweather_rain()
    radar_zones = analyze_radar_zones()

    # --- MESSAGE COMPOSE ---
    zone_messages = []
    rain_detected = False
    bar_data = []

    for zone in ZONES:
        status = radar_zones.get(zone, "clear")
        if status == "rain":
            zone_messages.append(f"📍 {zone}: 🌧️ Rain detected")
            bar_data.append((zone, 1.2))  # Assume ≥ 1 mm for radar detection
            rain_detected = True
        elif status == "cloud":
            zone_messages.append(f"📍 {zone}: ☁️ Overcast")
            bar_data.append((zone, 0.5))
        else:
            zone_messages.append(f"📍 {zone}: ☀️ Clear")
            bar_data.append((zone, 0.0))

    # --- SEND ALERTS ---
    if rain_forecast >= 1 or rain_detected:
        full_message = "🌧 Rain Alert: Possible rain over Mumbai!\n" + "\n".join(zone_messages)
        chart_line = generate_rainfall_chart([("Forecast", rain_forecast)], "live_line.png")
        chart_bar = generate_colored_bar_chart(bar_data, "live_bar.png")
        send_telegram_alert(full_message, [chart_line, chart_bar])
        send_email_alert("🌧 Rain Alert", full_message, [chart_line, chart_bar])
        return {"result": "🚨 Rain alert sent with charts"}
    else:
        full_message = "☀️ No rain alerts currently.\n" + "\n".join(zone_messages)
        send_telegram_alert(full_message)
        send_email_alert("☀️ No Rain Alert", full_message)
        return {"result": full_message}