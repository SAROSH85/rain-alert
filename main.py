from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data
from radar_quick_check import radar_quick_check

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Rain Alert API Running"}

@app.get("/alert/hourly")
@app.post("/alert/hourly")
def hourly_alert():
    """Runs the main rain analysis (your 30-min/hourly alert)."""
    return analyze_rain_data(mock=False)

@app.get("/alert/radar-quick")
@app.post("/alert/radar-quick")
def quick_radar_alert():
    """Runs the quick 10-min radar check."""
    return radar_quick_check()