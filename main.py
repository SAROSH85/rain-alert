from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Rain Alert API is live!"}

@app.get("/debug/env")
def debug_env():
    import os
    return {
        "TELEGRAM_BOT_TOKEN": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "EMAIL_SENDER": os.getenv("EMAIL_SENDER"),
        "EMAIL_RECEIVER": os.getenv("EMAIL_RECEIVER"),
    }
