from fastapi import FastAPI
from run_alert_if_time_matches import run
from hybrid_alert import analyze_rain_data
from radar_quick_check import radar_check

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "✅ Rain Alert system is live"}

@app.get("/alert/cron")
async def trigger_cron_alert():
    return run()

@app.get("/alert/send")
async def send_alert_now():
    result = analyze_rain_data()
    return {"manual_trigger": True, "result": result}
    
@app.post("/alert/timecheck")
async def alert_if_match():
    return run()
    
@app.get("/alert/radar-quick")
def quick_radar_alert():
    return radar_check()