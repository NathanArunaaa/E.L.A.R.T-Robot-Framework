import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

# Number of data points to show on the plot at once
MAX_DATA_POINTS = 20

def update_graph():
    # Generate random data for each series
    for j in range(len(data)):
        data[j].append(random.uniform(0, 10))  # Append a random value to each series

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
data = [[0], [0], [0], [0]]  # Initialize each series with one data point
colors = ['r', 'g', 'b', 'y']
labels = ['H2', 'CH4', 'Natural Gas', 'CO']
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

# Define the update function for the animation
def animate():
    update_graph()
    root.after(1000, animate)  # Update every 1 second (1000 milliseconds)

# Start the animation
animate()

root.mainloop()
