from fastapi import FastAPI, Request
from run_alert_if_time_matches import run
from hybrid_alert import analyze_rain_data
from radar_quick_check import quick_rain_check

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "✅ Rain Alert system is live"}

@app.post("/alert/cron")
@app.get("/alert/cron")
def alert_cron():
    return run()

@app.get("/alert/send")
async def send_alert_now():
    result = analyze_rain_data()
    return {"manual_trigger": True, "result": result}
    
@app.post("/alert/timecheck")
async def alert_if_match():
    return run()
    
@app.post("/alert/radar-quick")
@app.get("/alert/radar-quick")
def radar_quick():
    return radar_check()