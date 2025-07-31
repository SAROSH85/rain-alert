from datetime import datetime
import pytz

def get_server_time_info():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "server_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "hour": now.hour,
        "minute": now.minute
    }