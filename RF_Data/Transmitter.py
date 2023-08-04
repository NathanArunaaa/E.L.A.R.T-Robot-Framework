import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 12345)  # Replace 'x.x.x.x' with the IP address of the access point
client_socket.connect(server_address)

while True:
    data = client_socket.recv(1024).decode()
    if not data:
        break
    # Process the received data/command here
    print("Received:", data)

client_socket.close()