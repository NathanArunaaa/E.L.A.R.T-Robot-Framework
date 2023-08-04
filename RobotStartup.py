import socket
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
from io import BytesIO
import struct
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                data = client_socket.recv(4096)
                if not data:
                    break
                image_bytes += data
            
            if image_bytes:
                # Convert the received bytes to an ImageTk object
                image = Image.open(BytesIO(image_bytes))

                # Resize the image to fit the label
                label_width, label_height = camera_label.winfo_width(), camera_label.winfo_height()
                image = image.resize((label_width, label_height), Image.ANTIALIAS)

                # Convert the resized image to an ImageTk object
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

# Function to handle button clicks
def on_button_click(command):
    print(f"Sending command: {command}")
    send_command(command)

# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
host = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
port = 87     # Choose a port number for the communication
server_socket.bind((host, port))

# Start listening for incoming connections
server_socket.listen()

print("Waiting for connections...")

# Create the Tkinter GUI window
root = tk.Tk()
root.title("Robot Controller")

# Create the camera label to display the camera feed
camera_label = tk.Label(root)
camera_label.pack()

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

# Function to handle client connections
def handle_client(conn, addr):
    print("Client connected:", addr)
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            elif data == 'camera_frame':
                ret, frame = camera.read()
                if ret:
                    send_frame(conn, frame)
            else:
                # Process the received command
                print("Received command:", data)
                # Implement actions based on the received command
                # For example:
                if data == 'forward':
                    print("Moving forward")
                elif data == 'backward':
                    print("Moving backward")
                elif data == 'left':
                    print("Turning left")
                elif data == 'right':
                    print("Turning right")
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()
        print("Client disconnected:", addr)

# Function to send frames to the client
def send_frame(conn, frame):
    frame_data = pickle.dumps(frame)
    frame_size = struct.pack('!L', len(frame_data))
    conn.sendall(frame_size + frame_data)

# OpenCV Video Capture
camera = cv2.VideoCapture(0)  # Use 0 for the first camera device (change the index if needed)

try:
    while True:
        conn, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(conn, addr))
        client_handler.daemon = True
        client_handler.start()
except KeyboardInterrupt:
    print("Server stopped.")

# Release the camera and close the server socket
camera.release()
server_socket.close()

# Run the Tkinter event loop
root.mainloop()
