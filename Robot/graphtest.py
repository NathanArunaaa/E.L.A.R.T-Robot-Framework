import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Number of data points to show on the plot at once
MAX_DATA_POINTS = 20

# Gas concentration mean values
GAS_MEAN = {'H2': 0.09, 'CH4': 1.72, 'Natural Gas': 0.1, 'CO': 0.05}

def update_graph(i):
    # Generate random data for each series
    for j, gas in enumerate(GAS_MEAN.keys()):
        # Add random noise with deviation of +/- 0.5 to the mean value
        gas_concentration = GAS_MEAN[gas] + random.uniform(-0.5, 0.5)
        # Ensure the generated concentration is non-negative
        gas_concentration = max(gas_concentration, 0)
        data[j].append(gas_concentration)  # Append the generated concentration to each series

    # Trim data lists to keep only the latest MAX_DATA_POINTS
    for j in range(len(data)):
        data[j] = data[j][-MAX_DATA_POINTS:]

    # Update each line with new data
    for j in range(len(lines)):
        lines[j].set_data(list(range(len(data[j]))), data[j])

    # Calculate the maximum value in the data
    max_value = max(max(series) for series in data)

    # Adjust the y-axis limits to fit the new data
    ax.set_ylim(0, max_value + 1)  # Add a little buffer space

    # Adjust the x-axis limits to show only the last MAX_DATA_POINTS
    ax.set_xlim(max(0, len(data[0]) - MAX_DATA_POINTS), len(data[0]) + 1)

    canvas.draw()

root = tk.Tk()
root.title("E.L.A.R.T Real Time Gas Data")

fig, ax = plt.subplots()
data = [[] for _ in range(len(GAS_MEAN))]  # Initialize each series with an empty list
colors = ['r', 'g', 'b', 'y']
labels = list(GAS_MEAN.keys())  # Use the keys of GAS_MEAN as labels
lines = []

# Create lines for each series
for i in range(len(data)):
    line, = ax.plot([], [], color=colors[i], label=labels[i])  # Modify the label here
    lines.append(line)

ax.set_xlabel('X-axis')
ax.set_ylabel('PPM Gas Concentration')
ax.set_title('E.L.A.R.T Real Time Gas Data')
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

ani = FuncAnimation(fig, update_graph, interval=1000)  # Update every 1 second (1000 milliseconds)

root.mainloop()
