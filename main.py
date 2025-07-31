from fastapi import FastAPI
from hybrid_alert import analyze_rain_data
from run_alert_if_time_matches import run as run_time_check
from utils import get_server_time_info

app = FastAPI()


@app.get("/")
def root():
    return {"message": "☀️ Rain Alert System is running."}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.post("/alert/send")
async def send_alert():
    analyze_rain_data()
    return {"status": "✅ Alert process triggered successfully"}


@app.post("/alert/timecheck")
async def alert_if_match():
    return run_time_check()


@app.get("/debug/time")
def debug_time():
    return get_server_time_info()