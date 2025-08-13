import logging
import requests
import matplotlib.pyplot as plt
import os
from config import LAT, LON, OPENWEATHER_API_KEY
from fetch_radar import analyze_radar_zones
from notify import send_telegram_alert, send_email_alert

# ========== Chart Functions ==========
def generate_colored_bar_chart(data, filename="zones_bar.png"):
    zones = [z for z, _ in data]
    values = [v for _, v in data]
    colors = ["green" if v < 1 else "red" for v in values]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(zones, values, color=colors)
    plt.title("Zone-wise Rainfall Detection")
    plt.ylabel("Rainfall (mm)")
    plt.xticks(rotation=45, ha="right")

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, value + 0.05, f"{value:.1f}",
                 ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def generate_line_chart(data, filename="forecast_line.png"):
    times = [t for t, _ in data]
    values = [v for _, v in data]

    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o')
    plt.title("Hourly Rainfall Forecast")
    plt.xlabel("Time")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

# ========== Weather Fetch ==========
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

# ========== Main Analysis ==========
def analyze_rain_data(mock: bool = False):
    logging.info("🔄 Starting rain analysis...")

    if mock:
        logging.info("MOCK mode: generating fake rain alert.")
        forecast_data = [("12:00", 2), ("15:00", 5), ("18:00", 12)]
        radar_data = [("Zone1", 0.5), ("Zone2", 2)]
        chart1 = generate_line_chart(forecast_data, "mock_forecast.png")
        chart2 = generate_colored_bar_chart(radar_data, "mock_zones.png")
        send_telegram_alert("🌧 Mock Rain Alert", chart1, chart2)
        send_email_alert("🌧 Mock Rain Alert", "Mock data", chart1, chart2)
        return {"result": "✅ Mock alert sent"}

    # Fetch real data
    forecast_data = fetch_openweather_rain()
    radar_zones = analyze_radar_zones()

    rain_detected = any(v == "rain" for v in radar_zones.values()) or \
                    any(mm >= 1 for _, mm in forecast_data)

    if rain_detected:
        # Prepare radar chart data
        zone_chart_data = [(z, 1.0 if s == "rain" else 0.0) for z, s in radar_zones.items()]
        chart1 = generate_line_chart(forecast_data, "forecast_line.png")
        chart2 = generate_colored_bar_chart(zone_chart_data, "zones_bar.png")

        # Build message
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