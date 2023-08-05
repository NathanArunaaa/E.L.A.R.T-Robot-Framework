import socket
import tkinter as tk
import threading
import struct
import pickle
import cv2

class RobotControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Controller")

        self.camera_label = tk.Label(self)
        self.camera_label.pack()

        self.button_forward = tk.Button(self, text="Forward", command=self.on_forward)
        self.button_forward.pack()

        self.button_backward = tk.Button(self, text="Backward", command=self.on_backward)
        self.button_backward.pack()

        self.button_left = tk.Button(self, text="Left", command=self.on_left)
        self.button_left.pack()

        self.button_right = tk.Button(self, text="Right", command=self.on_right)
        self.button_right.pack()

        self.camera_thread = threading.Thread(target=self.update_camera_feed)
        self.camera_thread.daemon = True
        self.camera_thread.start()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.4.1', 87)  # Replace 'x.x.x.x' with the Raspberry Pi's IP address
        self.client_socket.connect(server_address)

    def on_forward(self):
        print("Sending command: forward")
        self.client_socket.sendall("forward".encode())

    def on_backward(self):
        print("Sending command: backward")
        self.client_socket.sendall("backward".encode())

    def on_left(self):
        print("Sending command: left")
        self.client_socket.sendall("left".encode())

    def on_right(self):
        print("Sending command: right")
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
                print("Received frame data:", len(frame_data), "bytes")

                # Convert the received bytes to a NumPy array
                frame = pickle.loads(frame_data)

                # Convert the NumPy array to an OpenCV image
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                # Display the video feed
                cv2.imshow("Camera Feed", frame)

            # Check for a key press (for closing the window gracefully)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

     except Exception as e:
        print("Error updating camera feed:", e)

     finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = RobotControllerApp()
    app.mainloop()
