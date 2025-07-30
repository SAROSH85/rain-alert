from datetime import datetime, timedelta
from hybrid_alert import analyze_rain_data

# List of trigger hours in IST
TRIGGER_HOURS = [9, 11, 13, 15, 17, 18, 19, 20]

def run():
    # Convert UTC to IST (+5:30)
    now_utc = datetime.utcnow()
    now_ist = now_utc + timedelta(hours=5, minutes=30)

    hour = now_ist.hour
    minute = now_ist.minute

    # Trigger at every 30th minute and only at specified hours
    if minute in [0, 30] and hour in TRIGGER_HOURS:
        result = analyze_rain_data()
        return {
            "triggered": True,
            "time": now_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "result": result
        }
    else:
        return {
            "triggered": False,
            "time": now_ist.strftime("%Y-%m-%d %H:%M:%S"),
            "reason": f"Not in TRIGGER_HOURS or not at 00 or 30 minutes (currently {hour}:{minute})"
        }