
from fastapi import FastAPI
from weather import check_rain_forecast
from telegram import send_telegram_message

app = FastAPI(title="Mumbai Rain Alert AI Agent")

@app.get("/")
def root():
    return {"message": "Mumbai Rain Alert AI Agent is running."}

@app.get("/rain-alert")
def rain_alert():
    rain_data = check_rain_forecast()

    if rain_data:
        msg = "🌧️ Rain Alert for Mumbai:\n" + "\n".join([f"{r['time']} – {r['amount_mm']} mm" for r in rain_data])
        send_telegram_message(msg)
        return {
            "status": "rain_expected",
            "forecast": rain_data,
            "message": msg
        }
    else:
        msg = "✅ No rain expected in the next 6 hours in Mumbai."
        send_telegram_message(msg)
        return {
            "status": "clear",
            "forecast": [],
            "message": msg
        }
