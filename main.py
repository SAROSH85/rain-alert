from fastapi import FastAPI, Request
from hybrid_alert import analyze_rain_data

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
    return {"message": "Rain Alert API is live!"}
