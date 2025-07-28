from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Rain Alert API is live!"}

@app.post("/alert/send")
async def send_alert(request: Request):
    body = await request.json()   # ✅ Fix: await is required
    mock = body.get("mock", False)
    result = analyze_rain_data(mock=mock)
    return result
