
import matplotlib.pyplot as plt
import os

def generate_rainfall_chart(rain_data, output_path="rainfall_chart.png"):
    """
    Generate a rainfall bar chart.
    
    Parameters:
    - rain_data: List of tuples like [("12 PM", 10), ("3 PM", 25)]
    - output_path: File path to save the chart image
    """

    if not rain_data:
        print("No rain data to plot.")
        return None

    # Extract times and rainfall values
    times = [x[0] for x in rain_data]
    values = [x[1] for x in rain_data]

    # Set color: green if <10mm, orange if <20mm, red otherwise
    colors = ['green' if val < 10 else 'orange' if val < 20 else 'red' for val in values]

    # Plot
    plt.figure(figsize=(8, 5))
    bars = plt.bar(times, values, color=colors)
    plt.title("Forecasted Rainfall")
    plt.xlabel("Time")
    plt.ylabel("Rainfall (mm)")
    plt.tight_layout()

    # Annotate bars
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(value),
                 ha='center', va='bottom', fontsize=8)

    # Save
    plt.savefig(output_path)
    plt.close()

    return output_path

def generate_line_chart(data, filename="line_chart.png"):
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