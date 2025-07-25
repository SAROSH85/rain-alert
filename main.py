# main.py

from fastapi import FastAPI
from hybrid_alert import analyze_rain_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "✅ Rain Alert Agent is live."}

@app.post("/alert/send")
def send_alert():
    """
    This endpoint triggers the hybrid rain alert analysis.
    It fetches data, analyzes, and sends updates via Telegram & Email.
    """
    result = analyze_rain_data()
    return {"result": result}