import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 87)  # Replace 'x.x.x.x' with the Raspberry Pi's IP address
client_socket.connect(server_address)

print('Connected to:', server_address)

while True:
    
    # Will be replaced with joystick input from raspberry pi
    command = input("Enter a command (forward, backward, left, right): ")
    
    # Send the command to the server
    client_socket.sendall(command.encode())

client_socket.close()
