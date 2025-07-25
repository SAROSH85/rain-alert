# hybrid_alert.py

from weather import fetch_nowcast, fetch_rainfall, fetch_forecast
from notify import send_telegram_alert, send_email_alert
from charts import generate_rainfall_chart

def analyze_rain_data():
    alert_msgs = []
    chart_img = None

    # 1. Check nowcast
    nowcast = fetch_nowcast()
    if nowcast:
        alert_msgs.append("🌧️ IMD Nowcast Alert:\n" + "\n".join([f"• {a}" for a in nowcast]))

    # 2. Check rainfall
    rainfall = fetch_rainfall()
    if rainfall:
        try:
            today = rainfall["today"]
            actual = float(today["actual"])
            normal = float(today["normal"])
            diff = actual - normal

            if diff > 3:
                status = "⚠️ Excess"
            elif diff < -3:
                status = "🔴 Deficit"
            else:
                status = "🟢 Normal"

            alert_msgs.append(f"📊 Rainfall Today: {actual}mm (Normal: {normal}mm) → {status}")
            chart_img = generate_rainfall_chart(actual, normal)
        except Exception as e:
            print("Rainfall parse error:", e)

    # 3. Forecast fallback
    forecast = fetch_forecast()
    if forecast:
        summary = "\n".join([f"🔮 {f}" for f in forecast])
        alert_msgs.append("📅 3-Day Forecast:\n" + summary)

    # 4. Final alert
    final_alert = "\n\n".join(alert_msgs) if alert_msgs else "☀️ No rain alerts or forecast available currently."

    # 5. Send alerts
    send_telegram_alert(final_alert, chart_img)
    send_email_alert("🌦️ Mumbai Rain Alert Update", final_alert, chart_img)
    return final_alert