from hybrid_alert import analyze_rain_data
from datetime import datetime

def run_scheduled_alert():
    """
    Always runs the rain alert check, no time/day restrictions.
    Returns the analysis result with a timestamp.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        result = analyze_rain_data()
        return {
            "triggered": True,
            "time": now,
            "result": result
        }
    except Exception as e:
        return {
            "triggered": False,
            "time": now,
            "error": str(e)
        }

if __name__ == "__main__":
    print(run_scheduled_alert())