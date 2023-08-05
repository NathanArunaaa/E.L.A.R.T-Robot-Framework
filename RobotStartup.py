import socket
import cv2
import threading
import struct
import pickle

# Function to send frames to the client
def send_frame(conn, frame):
    frame_data = pickle.dumps(frame)
    frame_size = struct.pack('!L', len(frame_data))
    conn.sendall(frame_size + frame_data)

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

# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
host = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
port = 12345     # Choose a port number for the communication
server_socket.bind((host, port))

# Start listening for incoming connections
server_socket.listen()

print("Waiting for connections...")

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
