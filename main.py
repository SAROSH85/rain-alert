from fastapi import FastAPI, Request
import logging
from hybrid_alert import analyze_rain_data

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/")
def home():
    return {"message": "Rain Alert API is live!"}

@app.post("/alert/send")
async def send_alert(request: Request):
    try:
        body = await request.json()
    except:
        body = {}

    mock = body.get("mock", False)
    result = analyze_rain_data(mock=mock)
    return result
