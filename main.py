from fastapi import FastAPI
from run_alert_if_time_matches import run_scheduled_alert
from radar_quick_check import radar_quick_check

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Rain Alert Service is running"}

# Endpoint for 30-min scheduled alert
@app.get("/alert/timecheck")
def timecheck_alert():
    try:
        return {"result": run_scheduled_alert()}
    except Exception as e:
        return {"error": str(e)}

# Endpoint for quick radar check every 10 min (≥1 mm rain filter is in radar_quick_check)
@app.get("/alert/radar-quick")
def radar_quick_alert():
    try:
        return {"result": radar_quick_check()}
    except Exception as e:
        return {"error": str(e)}

# Optional POST support
@app.post("/alert/timecheck")
def timecheck_alert_post():
    return timecheck_alert()

@app.post("/alert/radar-quick")
def radar_quick_alert_post():
    return radar_quick_alert()