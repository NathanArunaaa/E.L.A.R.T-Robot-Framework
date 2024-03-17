import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

# Number of data points to show on the plot at once
MAX_DATA_POINTS = 20

# Define the limits for each gas concentration
GAS_LIMITS = {
    'H2': (0, 10),
    'CH4': (0, 10),
    'Natural Gas': (0, 10),
    'CO': (0, 10)
}

def generate_gas_data():
    gas_data = {}
    for gas, (lower_limit, upper_limit) in GAS_LIMITS.items():
        gas_data[gas] = random.uniform(lower_limit, upper_limit)
    return gas_data

def update_graph():
    # Generate random data for each gas series
    gas_data = generate_gas_data()

    # Append the new data to each gas series
    for i, gas in enumerate(data.keys()):
        data[gas].append(gas_data[gas])

        # Trim data lists to keep only the latest MAX_DATA_POINTS
        data[gas] = data[gas][-MAX_DATA_POINTS:]

        # Update each line with new data
        lines[i].set_data(list(range(len(data[gas]))), data[gas])

    # Calculate the maximum value in the data
    max_value = max(max(series) for series in data.values())

    # Adjust the y-axis limits to fit the new data
    ax.set_ylim(0, max_value + 1)  # Add a little buffer space

    # Adjust the x-axis limits to show only the last MAX_DATA_POINTS
    ax.set_xlim(max(0, len(data['H2']) - MAX_DATA_POINTS), len(data['H2']) + 1)

    canvas.draw()

root = tk.Tk()
root.title("E.L.A.R.T Real Time Gas Data")

fig, ax = plt.subplots()
data = {gas: [0] for gas in GAS_LIMITS.keys()}  # Initialize each gas series with one data point
colors = ['r', 'g', 'b', 'y']
labels = list(GAS_LIMITS.keys())
lines = []

# Create lines for each gas series
for i, gas in enumerate(data.keys()):
    line, = ax.plot([], [], color=colors[i], label=gas)
    lines.append(line)

ax.set_xlabel('X-axis')
ax.set_ylabel('PPM Gas Concentration')
ax.set_title('E.L.A.R.T Real Time Gas Data')
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Define the animation function
def animate():
    update_graph()
    root.after(1000, animate)  # Update every 1 second (1000 milliseconds)

# Start the animation
animate()

root.mainloop()
