import datetime
import requests

# Your deployed app URL
ENDPOINT = "https://rain-alert-eagu.onrender.com/alert/send"

# IST Timezone = UTC+5:30
TRIGGER_HOURS = [9, 11, 13, 15, 17, 18, 19, 20]  # IST hours

def is_trigger_time():
    now_utc = datetime.datetime.utcnow()
    now_ist = now_utc + datetime.timedelta(hours=5, minutes=30)
    return now_ist.hour in TRIGGER_HOURS

def run():
    if is_trigger_time():
        print("✅ Triggering rain alert...")
        r = requests.post(ENDPOINT)
        print(f"✅ Response {r.status_code}: {r.text}")
    else:
        print("⏳ Not a trigger time. Skipping.")

if __name__ == "__main__":
    run()