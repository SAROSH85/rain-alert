
# formatter.py

def format_zone_alerts(zone_analysis: dict) -> str:
    lines = [f"📍 {zone}: {status}" for zone, status in zone_analysis.items()]
    return "\n".join(lines)
