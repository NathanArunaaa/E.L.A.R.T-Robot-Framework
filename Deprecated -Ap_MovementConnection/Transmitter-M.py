import socket
import tkinter as tk

# Function to send commands to the server
def send_command(command):
    client_socket.sendall(command.encode())

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 85)  # Replace 'x.x.x.x' with the Raspberry Pi's IP address
client_socket.connect(server_address)

# Create the Tkinter GUI window
root = tk.Tk()
root.title("Robot Controller")

# Function to handle button clicks
def on_button_click(command):
    print(f"Sending command: {command}")
    send_command(command)

# Create buttons for different commands
button_forward = tk.Button(root, text="Forward", command=lambda: on_button_click("forward"))
button_forward.pack()

button_backward = tk.Button(root, text="Backward", command=lambda: on_button_click("backward"))
button_backward.pack()

button_left = tk.Button(root, text="Left", command=lambda: on_button_click("left"))
button_left.pack()

button_right = tk.Button(root, text="Right", command=lambda: on_button_click("right"))
button_right.pack()

# Run the Tkinter event loop
root.mainloop()
