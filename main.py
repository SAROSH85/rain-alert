# main.py

from fastapi import FastAPI
from hybrid_alert import analyze_rain_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🌦️ Rain Alert Agent is live!"}

@app.post("/alert/send")
def send_alert():
    result = analyze_rain_data()
    return {"status": "sent", "message": result}