from fastapi import FastAPI
from hybrid_alert import analyze_rain_data
from radar_quick_check import radar_quick_check

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "Rain Alert API running"}

@app.get("/alert/full")
@app.post("/alert/full")
def full_alert():
    return analyze_rain_data(mock=False)

@app.get("/alert/radar-quick")
@app.post("/alert/radar-quick")
def quick_alert():
    return radar_quick_check()