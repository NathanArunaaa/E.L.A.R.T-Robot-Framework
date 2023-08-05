import socket
import tkinter as tk
from PIL import Image, ImageTk
import threading
import struct
import pickle
import cv2

class RobotControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Controller")

        self.camera_frame = tk.Frame(self)
        self.camera_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_forward = tk.Button(self.button_frame, text="Forward", command=self.on_forward)
        self.button_forward.pack(pady=5)

        self.button_backward = tk.Button(self.button_frame, text="Backward", command=self.on_backward)
        self.button_backward.pack(pady=5)

        self.button_left = tk.Button(self.button_frame, text="Left", command=self.on_left)
        self.button_left.pack(pady=5)

        self.button_right = tk.Button(self.button_frame, text="Right", command=self.on_right)
        self.button_right.pack(pady=5)

        self.camera_thread = threading.Thread(target=self.update_camera_feed)
        self.camera_thread.daemon = True
        self.camera_thread.start()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.4.1', 87)  # Replace 'x.x.x.x' with the Raspberry Pi's IP address
        self.client_socket.connect(server_address)

    # Implement the on_forward, on_backward, on_left, and on_right methods as before
    def on_forward(self):
        # Send the forward command to the robot
        self.client_socket.sendall("forward".encode())

    def on_backward(self):
        # Send the backward command to the robot
        self.client_socket.sendall("backward".encode())

    def on_left(self):
        # Send the left command to the robot
        self.client_socket.sendall("left".encode())

    def on_right(self):
        # Send the right command to the robot
        self.client_socket.sendall("right".encode())
    def update_camera_feed(self):
        try:
            while True:
                # Request camera frame from the server
                self.client_socket.sendall("camera_frame".encode())
                frame_size_data = self.client_socket.recv(4)
                if not frame_size_data:
                    break
                frame_size = struct.unpack('!L', frame_size_data)[0]
                frame_data = b''
                while len(frame_data) < frame_size:
                    data = self.client_socket.recv(frame_size - len(frame_data))
                    if not data:
                        break
                    frame_data += data

                if len(frame_data) == frame_size:
                    # Convert the received bytes to a NumPy array
                    frame = pickle.loads(frame_data)

                    # Convert the NumPy array to an OpenCV image
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                    # Convert the OpenCV image to a PIL Image
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)

                    # Resize the image to fit the label
                    label_width, label_height = self.camera_label.winfo_width(), self.camera_label.winfo_height()
                    image = image.resize((label_width, label_height), Image.ANTIALIAS)

                    # Convert the resized image to a PhotoImage object
                    image_tk = ImageTk.PhotoImage(image)

                    # Update the label with the new image
                    self.camera_label.config(image=image_tk)
                    self.camera_label.image = image_tk  # Store the reference to avoid garbage collection

        except Exception as e:
            print("Error updating camera feed:", e)

if __name__ == "__main__":
    app = RobotControllerApp()
    app.mainloop()
