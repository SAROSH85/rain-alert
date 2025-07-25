from weather import fetch_nowcast, fetch_rainfall, fetch_forecast
from notify import send_telegram_alert, send_email_alert
from charts import generate_rainfall_chart

def analyze_rain_data(mock=False):
    if mock:
        message = (
            "🌧️ *Mock Rain Alert*: Simulated heavy rainfall detected in Mumbai.\n"
            "Take precautions. Stay safe! 🚨"
        )
        chart_path = "mock_rainfall_chart.png"
        send_telegram_alert(message, chart_path)
        send_email_alert("Mock Rain Alert 🚨", message)
        return "✅ Mock alert sent"

    nowcast = fetch_nowcast()
    rainfall = fetch_rainfall()
    forecast = fetch_forecast()

    alert_parts = []

    if nowcast:
        alert_parts.append("📡 *Nowcast:* " + nowcast)

    if rainfall:
        alert_parts.append("🌧️ *Rainfall Radar:* " + rainfall)

    if forecast:
        alert_parts.append("📅 *Forecast:* " + forecast)

    if not alert_parts:
        return "☀️ No rain alerts or forecast available currently."

    final_alert = "\n\n".join(alert_parts)
    chart_img = generate_rainfall_chart()

    send_telegram_alert(final_alert, chart_img)
    send_email_alert("Hybrid Rain Alert 🚨", final_alert)

    return "✅ Hybrid alert sent"