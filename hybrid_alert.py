import logging
import requests
from charts import generate_rainfall_chart, generate_colored_bar_chart, generate_line_chart
from notify import send_telegram_alert, send_email_alert
from config import LAT, LON, OPENWEATHER_API_KEY
from fetch_radar import analyze_radar_zones

def fetch_openweather_rain():
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": LAT,
            "lon": LON,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        hourly_data = []
        for entry in data["list"][:6]:  # Next 6 hours
            time_str = entry["dt_txt"].split(" ")[1][:5]
            rain_mm = entry.get("rain", {}).get("3h", 0) / 3  # Convert 3h to 1h avg
            hourly_data.append((time_str, round(rain_mm, 1)))

        return hourly_data
    except Exception as e:
        logging.error(f"OpenWeather API error: {e}")
        return []

def analyze_rain_data(mock: bool = False):
    logging.info("🔄 Starting rain analysis...")

    if mock:
        logging.info("MOCK mode: generating fake rain alert.")
        rain_data = [("12:00", 2), ("15:00", 5), ("18:00", 12)]
        chart1 = generate_rainfall_chart(rain_data, "mock_forecast.png")
        chart2 = generate_colored_bar_chart([("Zone1", 0.5), ("Zone2", 2)], "mock_zones.png")
        send_telegram_alert("🌧 Mock Rain Alert", chart1, chart2)
        send_email_alert("🌧 Mock Rain Alert", "Mock data", chart1, chart2)
        return {"result": "✅ Mock alert sent"}

    forecast_data = fetch_openweather_rain()
    radar_zones = analyze_radar_zones()

    rain_detected = any(v == "rain" for v in radar_zones.values()) or any(mm >= 1 for _, mm in forecast_data)

    if rain_detected:
        zone_chart_data = [(z, 1.0 if s == "rain" else 0.0) for z, s in radar_zones.items()]
        chart1 = generate_line_chart(forecast_data, "forecast_line.png")
        chart2 = generate_colored_bar_chart(zone_chart_data, "zones_bar.png")

        message = "🌧 Rain Alert: Possible rain over Mumbai!\n"
        for zone, status in radar_zones.items():
            emoji = "🌧️" if status == "rain" else "☁️" if status == "cloud" else "☀️"
            message += f"📍 {zone}: {emoji} {status}\n"

        send_telegram_alert(message, chart1, chart2)
        send_email_alert("🌧 Rain Alert", message, chart1, chart2)
        return {"result": "🚨 Rain alert sent"}
    else:
        message = "☀️ No rain detected in forecast or radar."
        send_telegram_alert(message)
        send_email_alert("☀️ No Rain Alert", message)
        return {"result": message}