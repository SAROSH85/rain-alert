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

# 🔍 DEBUG ENV ENDPOINT
@app.get("/debug/env")
async def debug_env():
    return {
        "EMAIL_SENDER": EMAIL_SENDER,
        "EMAIL_PASSWORD_PRESENT": bool(EMAIL_PASSWORD),
        "EMAIL_RECEIVER": EMAIL_RECEIVER
    }