from fastapi import FastAPI
from run_alert_if_time_matches import run_scheduled_alert
from radar_quick_check import radar_quick_check

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Rain Alert Service is running"}

# Original scheduled alert
@app.get("/alert/timecheck")
def timecheck_alert():
    try:
        result = run_scheduled_alert()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Quick radar check every 10 minutes for ≥ 1mm rain
@app.get("/alert/radar-quick")
def radar_quick_alert():
    try:
        result = radar_quick_check()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Optional POST support for automation tools
@app.post("/alert/timecheck")
def timecheck_alert_post():
    return timecheck_alert()

@app.post("/alert/radar-quick")
def radar_quick_alert_post():
    return radar_quick_alert()