from datetime import datetime, timedelta
from hybrid_alert import analyze_rain_data

# List of trigger hours in IST (hourly from 9 AM to 11 PM)
TRIGGER_HOURS = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

def run():
    # Convert UTC to IST (+5:30)
    now_utc = datetime.utcnow()
    now_ist = now_utc + timedelta(hours=5, minutes=30)

    hour = now_ist.hour
    minute = now_ist.minute

    # Trigger only at start of the hour
    if minute == 0 and hour in TRIGGER_HOURS:
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
            "reason": f"Not in TRIGGER_HOURS or not at 00 minutes (currently {hour}:{minute})"
        }