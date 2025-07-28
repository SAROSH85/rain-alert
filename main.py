from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Rain Alert API is live!"}

@app.post("/alert/send")
def send_alert(request: Request):
    body = request.json() if request.body() else {}
    mock = body.get("mock", False)
    return analyze_rain_data(mock=mock)
