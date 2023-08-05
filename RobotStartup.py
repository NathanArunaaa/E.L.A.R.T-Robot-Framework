import socket
import threading
import struct
import pickle
import cv2

def handle_client(conn, addr):
    print("Client connected:", addr)

    cap = cv2.VideoCapture(0)  # Use 0 for the first USB camera, 1 for the second, and so on
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Adjust the resolution as needed
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            elif data == 'camera_frame':
                ret, frame = cap.read()
                if ret:
                    # Convert the frame to a byte array
                    frame_data = pickle.dumps(frame)

                    # Send the size of the frame first
                    frame_size = len(frame_data)
                    conn.sendall(struct.pack('!L', frame_size))

                    # Send the frame data
                    conn.sendall(frame_data)
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
        conn.close()
        print("Client disconnected:", addr)

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 87)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Waiting for connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()
