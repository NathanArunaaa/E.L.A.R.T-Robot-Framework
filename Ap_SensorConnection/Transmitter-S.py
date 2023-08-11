import socket
import time
import subprocess
import threading

def sensor_thread():
    # Set up a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 86)  # Replace with your server's IP and port
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Sensor Script: Waiting for controller connection...")
    try:
        while True:
            conn, addr = server_socket.accept()
            print("Sensor Script: Connected to:", addr)

            while True:
                result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
                temperature_str = result.stdout.strip()
                temperature = float(temperature_str.split('=')[1].replace("'C", ""))
                temperature_data = f"Sensor data: {temperature:.2f} °C"

                # Send sensor data to the controller
                try:
                    conn.sendall(temperature_data.encode())
                except (BrokenPipeError, ConnectionResetError):
                    print("Sensor Script: Client disconnected.")
                    break

                time.sleep(1)  # Adjust the delay based on your requirements

            conn.close()
            print("Sensor Script: Connection closed.")

    finally:
        server_socket.close()

# Start the sensor thread
sensor_thread = threading.Thread(target=sensor_thread)
sensor_thread.start()
