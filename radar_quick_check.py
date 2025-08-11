import os
import requests
from fetch_radar import analyze_radar_image, ZONES
from notify import send_telegram_alert, send_email_alert
from tabulate import tabulate

# Official IMD radar sources
SRI_URL = "https://mausam.imd.gov.in/Radar/sri_vrv.gif"
PAC_URL = "https://mausam.imd.gov.in/Radar/pac_vrv.gif"

RAIN_THRESHOLD_MM = 1.0  # Minimum rain to trigger alert

def radar_quick_check():
    try:
        # Download SRI
        sri_resp = requests.get(SRI_URL, timeout=15)
        sri_resp.raise_for_status()
        with open("sri.gif", "wb") as f:
            f.write(sri_resp.content)

        # Download PAC
        pac_resp = requests.get(PAC_URL, timeout=15)
        pac_resp.raise_for_status()
        with open("pac.gif", "wb") as f:
            f.write(pac_resp.content)

        # Analyze images for all zones
        sri_data = analyze_radar_image("sri.gif", ZONES)
        pac_data = analyze_radar_image("pac.gif", ZONES)

        table_data = []
        for zone in ZONES.keys():
            sri_mm = sri_data.get(zone, 0)
            pac_mm = pac_data.get(zone, 0)
            if sri_mm >= RAIN_THRESHOLD_MM and pac_mm >= RAIN_THRESHOLD_MM:
                table_data.append([zone, f"{sri_mm:.1f}", f"{pac_mm:.1f}"])

        # If no alerts, do nothing
        if not table_data:
            return {"status": "no_alert", "alerts": []}

        # Prepare message
        header = "🚨 Quick Rain Alert (≥ 1 mm in both SRI & PAC)\n"
        table_str = tabulate(table_data, headers=["Zone", "SRI mm", "PAC mm"], tablefmt="grid")

        alert_msg = f"{header}\n```\n{table_str}\n```"

        # Send alerts
        send_telegram_alert(alert_msg)
        send_email_alert("Quick Rain Alert", f"{header}\n{table_str}")

        return {"status": "alert_sent", "alerts": table_data}

    except Exception as e:
        return {"status": "error", "message": str(e)}