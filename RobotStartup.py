import socket
import threading
import cv2
import struct
import pickle

# Function to send camera frames to the client
def send_frame(conn, frame):
    frame_data = pickle.dumps(frame)
    frame_size = struct.pack('!L', len(frame_data))
    conn.sendall(frame_size + frame_data)

# Function to handle client connections
def handle_client(conn, addr):
    print("Client connected:", addr)
    try:
        cap = cv2.VideoCapture(0)  # Use 0 for the first USB camera, 1 for the second, and so on
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Adjust the resolution as needed
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            elif data == 'camera_frame':
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Camera Feed', frame)
                    cv2.waitKey(1)
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
        cap.release()
        cv2.destroyAllWindows()
        conn.close()
        print("Client disconnected:", addr)


# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 87)  # Use an empty string to listen on all available interfaces
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is listening for incoming connections...")
    while True:
        conn, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(conn, addr))
        client_handler.daemon = True
        client_handler.start()

if __name__ == "__main__":
    start_server()
