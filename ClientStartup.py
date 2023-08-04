import socket
import tkinter as tk
from PIL import Image, ImageTk
import threading
from io import BytesIO

# Function to send commands to the server
def send_command(command):
    client_socket.sendall(command.encode())

# Function to update the camera feed
def update_camera_feed():
    try:
        while True:
            # Request camera frame from the server
            client_socket.sendall("camera_frame".encode())
            image_bytes = b''
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                image_bytes += data
            
            if image_bytes:
                # Convert the received bytes to an ImageTk object
                image = Image.open(BytesIO(image_bytes))
                image = ImageTk.PhotoImage(image)
                
                # Update the label with the new image
                camera_label.config(image=image)
                camera_label.image = image
    except Exception as e:
        print("Error updating camera feed:", e)

# Function to start the camera feed thread
def start_camera_thread():
    camera_thread = threading.Thread(target=update_camera_feed)
    camera_thread.daemon = True
    camera_thread.start()

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

# Start the camera feed thread
start_camera_thread()

# Run the Tkinter event loop
root.mainloop()
