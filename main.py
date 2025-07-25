from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Rain Alert API is live!"}

@app.post("/alert/send")
async def send_alert(request: Request):
    try:
        data = await request.json()
        mock = data.get("mock", False)
    except:
        mock = False  # fallback if no JSON payload is provided

    result = analyze_rain_data(mock=mock)
    return {"result": result}