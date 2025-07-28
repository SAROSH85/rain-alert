import logging
from charts import generate_rainfall_chart
from notify import send_telegram_alert, send_email_alert

def analyze_rain_data(mock: bool = False):
    logging.info("🔄 Analyzing rain data...")

    if mock:
        logging.info("🔄 MOCK mode: Generating a fake rain alert.")
        rain_data = [("Hour 1", 10), ("Hour 2", 20), ("Hour 3", 30)]
        chart_path = generate_rainfall_chart(rain_data, "mock_chart.png")

        alert_message = "🌧 Mock Rain Alert: Simulated heavy rainfall detected in Mumbai.\nTake precautions. Stay safe! 🚨"

        send_telegram_alert(alert_message, chart_path)
        send_email_alert("🌧 Mock Rain Alert", alert_message, chart_path)

        return {"result": "✅ Mock alert sent"}

    return {"result": "☀️ No rain alerts or forecast available currently."}
