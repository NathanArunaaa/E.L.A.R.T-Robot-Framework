import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
host = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
port = 12345     # Choose a port number for the communication
server_socket.bind((host, port))

# Start listening for incoming connections
server_socket.listen(1)

print("Waiting for a connection...")
conn, addr = server_socket.accept()
print("Connected to:", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    # Process the received data/command here
    print("Received:", data)

conn.close()
