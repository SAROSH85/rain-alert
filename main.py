from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER
from run_alert_if_time_matches import run

app = FastAPI()

@app.post("/alert/send")
async def send_alert(request: Request):
    try:
        try:
            body = await request.json()
        except Exception:
            body = {}
        mock = body.get("mock", False)
        result = analyze_rain_data(mock=mock)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.api_route("/alert/timecheck", methods=["GET", "POST"])
async def alert_if_match():
    return run()

@app.get("/")
async def root():
    return {"result": "☀️ No rain alerts or forecast available currently."}

# Optional: debug endpoint
@app.get("/debug/email")
async def debug_email_config():
    return {
        "EMAIL_SENDER": EMAIL_SENDER,
        "EMAIL_RECEIVER": EMAIL_RECEIVER,
        "EMAIL_PASSWORD_PRESENT": bool(EMAIL_PASSWORD),
        "EMAIL_PASSWORD_PREVIEW": EMAIL_PASSWORD[:4] + "****" + EMAIL_PASSWORD[-2:] if EMAIL_PASSWORD else None
    }

@app.get("/debug/time")
async def debug_time():
    from datetime import datetime
    import pytz
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "server_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "hour": now.hour,
        "minute": now.minute
    }