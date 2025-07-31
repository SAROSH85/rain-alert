
from datetime import datetime
from zoneinfo import ZoneInfo

def get_server_time_info():
    ist = ZoneInfo("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "server_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "hour": now.hour,
        "minute": now.minute
    }
