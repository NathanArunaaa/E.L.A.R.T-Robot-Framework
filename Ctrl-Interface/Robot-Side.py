#E.L.A.R.T Controller Reciever(robot side) By: Nathan Aruna

import socket
import cv2
import threading
import struct
import pickle
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)


# Function to send frames to the client
def send_frame(conn, frame):
    frame_data = pickle.dumps(frame)
    frame_size = struct.pack('!L', len(frame_data))
    conn.sendall(frame_size + frame_data)

def sysReboot():
    print('System Rebooting....')
    time.sleep(5)
    os.system('sudo reboot')

def sysShutdown():
    print('System Shutdown....')
    time.sleep(5)
    os.system('sudo shutdown')
    
def ledOn():
    while True:
        # set GPIO14 pin to HIGH
        GPIO.output(14,GPIO.HIGH)
        # show message to Terminal
        print ("LED is ON")
        # pause for one second
        time.sleep(1)

        # set GPIO14 pin to HIGH
        GPIO.output(14,GPIO.LOW)
        # show message to Terminal
        print("LED is OFF")
        # pause for one second
        time.sleep(1)
    


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
                print("Received command:", data)
                # Checking for commands from the controller
              
                if data == 'reboot':
                    sysReboot()
                    
                elif data == 'shutdown':
                    sysShutdown()
                    
                elif data == 'nav1':
                    #add logic to turn on navigation lights
                    print("Turning On Navigation Lights 1")
                    
                elif data == 'auto':
                    #add logic to turn on auto mode
                    print("Auto Mode On")
                    
                elif data == 'overide':
                    #add logic to turn on overide mode
                    print("Overide Mode On")
                    
                elif data == 'nav2':
                    #add logic to turn on navigation lights
                    print("Turning On Navigation Lights 2")
                    
                elif data == 'headlight1':
                    #add logic to turn on headlights
                    print("Turning On Headlights 1")
                    
                elif data == 'headlight2':
                    #add logic to turn on headlights
                    print("Turning On Headlights 2")
                
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()
        print("Client disconnected:", addr)

# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
host = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
port = 87    # Choose a port number for the communication
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
