import socket
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import time

# Function to send commands to the server
def send_command(command):
    client_socket.sendall(command.encode())

# Function to update the camera feed
def update_camera_feed():
    try:
        # Request camera frame from the server
        client_socket.sendall("camera_frame".encode())
        image_bytes = b''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            image_bytes += data
        
        if image_bytes:
            # Convert the received bytes to an ImageTk object and update the label
            image = Image.open(BytesIO(image_bytes))
            image = ImageTk.PhotoImage(image)
            camera_label.config(image=image)
            camera_label.image = image
    except Exception as e:
        print("Error updating camera feed:", e)
    
    # Schedule the update after 100 milliseconds
    root.after(100, update_camera_feed)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 87)  # Replace 'x.x.x.x' with the Raspberry Pi's IP address
client_socket.connect(server_address)

# Create the Tkinter GUI window
root = tk.Tk()
root.title("Robot Controller")

# Create the camera label to display the camera feed
camera_label = tk.Label(root)
camera_label.pack()

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

# Start updating the camera feed
update_camera_feed()

# Run the Tkinter event loop
root.mainloop()
