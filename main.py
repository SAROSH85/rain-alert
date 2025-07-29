from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

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

@app.get("/")
async def root():
    return {"result": "☀️ No rain alerts or forecast available currently."}

# 🔍 DEBUG: Check loaded env vars
@app.get("/debug/env")
async def debug_env():
    return {
        "EMAIL_SENDER": EMAIL_SENDER,
        "EMAIL_PASSWORD_PRESENT": bool(EMAIL_PASSWORD),
        "EMAIL_RECEIVER": EMAIL_RECEIVER
    }

# 🔍 DEBUG: Show masked password
@app.get("/debug/email")
async def debug_email_config():
    return {
        "EMAIL_SENDER": EMAIL_SENDER,
        "EMAIL_RECEIVER": EMAIL_RECEIVER,
        "EMAIL_PASSWORD_PRESENT": bool(EMAIL_PASSWORD),
        "EMAIL_PASSWORD_PREVIEW": EMAIL_PASSWORD[:4] + "****" + EMAIL_PASSWORD[-2:] if EMAIL_PASSWORD else None
    }