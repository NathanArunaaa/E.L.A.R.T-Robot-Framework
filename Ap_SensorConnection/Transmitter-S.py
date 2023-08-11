import socket
import time
import subprocess


# Set up a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 86)  # Replace with your server's IP and port
server_socket.bind(server_address)
server_socket.listen(1)

print("Waiting for controller connection...")
conn, addr = server_socket.accept()
print("Connected to:", addr)

try:
    while True:
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        temperature_str = result.stdout.strip()
        temperature = float(temperature_str.split('=')[1].replace("'C", ""))
        temperature = "Sensor data: "  # Replace with actual sensor reading

        # Send sensor data to the controller
        conn.sendall(temperature.encode())
        time.sleep(1)  # Adjust the delay based on your requirements
finally:
    conn.close()
