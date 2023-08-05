import socket
import tkinter as tk
from PIL import Image, ImageTk
import threading
from io import BytesIO
import struct
import pickle

# Function to update the camera feed
def update_camera_feed():
    try:
        while True:
            # Request camera frame from the server
            client_socket.sendall("camera_frame".encode())
            frame_size_data = client_socket.recv(4)
            if not frame_size_data:
                break
            frame_size = struct.unpack('!L', frame_size_data)[0]
            frame_data = b''
            while len(frame_data) < frame_size:
                data = client_socket.recv(frame_size - len(frame_data))
                if not data:
                    break
                frame_data += data

            if len(frame_data) == frame_size:
                # Convert the received bytes to a NumPy array
                frame = pickle.loads(frame_data)

                # Convert the NumPy array to an ImageTk object
                image = Image.fromarray(frame)

                # Resize the image to fit the label
                label_width, label_height = camera_label.winfo_width(), camera_label.winfo_height()
                image = image.resize((1200, 780), Image.ANTIALIAS)

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

# Function to send commands to the server
def on_button_click(command):
    print(f"Sending command: {command}")
    client_socket.sendall(command.encode())

# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 87)  # Replace 'x.x.x.x' with the Raspberry Pi's IP address
client_socket.connect(server_address)

# Create a Tkinter GUI window
root = tk.Tk()
root.title("E.L.A.R.T - Controller")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT)

button_forward = tk.Button(left_frame, text="Forward", command=lambda: on_button_click("forward"))
button_forward.pack(side=tk.TOP, padx=5, pady=5)

button_backward = tk.Button(left_frame, text="Backward", command=lambda: on_button_click("backward"))
button_backward.pack(side=tk.TOP, padx=5, pady=5)

button_left = tk.Button(left_frame, text="Left", command=lambda: on_button_click("left"))
button_left.pack(side=tk.TOP, padx=5, pady=5)

button_right = tk.Button(left_frame, text="Right", command=lambda: on_button_click("right"))
button_right.pack(side=tk.TOP, padx=5, pady=5)

# Create the camera label to display the camera feed
camera_label = tk.Label(root, text="Camera View")
camera_label.pack(side=tk.LEFT, padx=5, pady=5)

# Create the frame for the right column of buttons
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT)

button_forward = tk.Button(right_frame, text="Forward", command=lambda: on_button_click("forward"))
button_forward.pack(side=tk.TOP, padx=5, pady=5)

button_backward = tk.Button(right_frame, text="Backward", command=lambda: on_button_click("backward"))
button_backward.pack(side=tk.TOP, padx=5, pady=5)

button_left = tk.Button(right_frame, text="Left", command=lambda: on_button_click("left"))
button_left.pack(side=tk.TOP, padx=5, pady=5)

button_right = tk.Button(right_frame, text="Right", command=lambda: on_button_click("right"))
button_right.pack(side=tk.TOP, padx=5, pady=5)




# Create buttons for different commands


# Start the camera feed thread
start_camera_thread()

# Run the Tkinter event loop
root.mainloop()
