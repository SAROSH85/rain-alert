import matplotlib.pyplot as plt

def generate_rainfall_chart(rain_data, output_path="rainfall_chart.png"):
    """
    Forecast bar chart:
    - Green if <10mm
    - Orange if 10–20mm
    - Red if ≥20mm
    """
    if not rain_data:
        print("No rain data to plot.")
        return None

    times = [x[0] for x in rain_data]
    values = [x[1] for x in rain_data]
    colors = ['green' if val < 10 else 'orange' if val < 20 else 'red' for val in values]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(times, values, color=colors)
    plt.title("Forecasted Rainfall")
    plt.xlabel("Time")
    plt.ylabel("Rainfall (mm)")
    plt.tight_layout()

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(value),
                 ha='center', va='bottom', fontsize=8)

    plt.savefig(output_path)
    plt.close()
    return output_path


def generate_colored_bar_chart(zone_data, output_path="zone_rain_chart.png"):
    """
    Zone-wise radar bar chart:
    - Green if <1mm
    - Red if ≥1mm
    """
    if not zone_data:
        print("No zone data to plot.")
        return None

    zones = [x[0] for x in zone_data]
    values = [x[1] for x in zone_data]
    colors = ['green' if val < 1 else 'red' for val in values]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(zones, values, color=colors)
    plt.title("Zone-wise Rainfall Detection")
    plt.xlabel("Zones")
    plt.ylabel("Rainfall (mm)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{value:.1f}", ha='center', va='bottom', fontsize=8)

    plt.savefig(output_path)
    plt.close()
    return output_path


def generate_line_chart(data, filename="line_chart.png"):
    """
    Hourly forecast line chart.
    """
    if not data:
        print("No data to plot.")
        return None

    hours = [item[0] for item in data]
    values = [item[1] for item in data]

    plt.figure(figsize=(10, 5))
    plt.plot(hours, values, marker='o')
    plt.title("Hourly Rainfall Forecast")
    plt.xlabel("Time")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename