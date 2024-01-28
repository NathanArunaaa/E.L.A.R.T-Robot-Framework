import socket
import RPi.GPIO as GPIO
import time

# Set up GPIO pins for robot movement
GPIO.setmode(GPIO.BCM)

# Replace the following pin numbers with the actual GPIO pins connected to the robot's motors
motor_a_forward_pin = 17
motor_a_backward_pin = 18
motor_b_forward_pin = 22
motor_b_backward_pin = 23

GPIO.setup(motor_a_forward_pin, GPIO.OUT)
GPIO.setup(motor_a_backward_pin, GPIO.OUT)
GPIO.setup(motor_b_forward_pin, GPIO.OUT)
GPIO.setup(motor_b_backward_pin, GPIO.OUT)

# Function to control the robot's movement
def move_forward():
    print("Moving forward")
    GPIO.output(motor_a_forward_pin, GPIO.HIGH)
    GPIO.output(motor_a_backward_pin, GPIO.LOW)
    GPIO.output(motor_b_forward_pin, GPIO.HIGH)
    GPIO.output(motor_b_backward_pin, GPIO.LOW)

def move_backward():
    print("Moving backward")
    GPIO.output(motor_a_forward_pin, GPIO.LOW)
    GPIO.output(motor_a_backward_pin, GPIO.HIGH)
    GPIO.output(motor_b_forward_pin, GPIO.LOW)
    GPIO.output(motor_b_backward_pin, GPIO.HIGH)

def turn_left():
    print("Turning left")
    GPIO.output(motor_a_forward_pin, GPIO.LOW)
    GPIO.output(motor_a_backward_pin, GPIO.HIGH)
    GPIO.output(motor_b_forward_pin, GPIO.HIGH)
    GPIO.output(motor_b_backward_pin, GPIO.LOW)

def turn_right():
    print("Turning right")
    GPIO.output(motor_a_forward_pin, GPIO.HIGH)
    GPIO.output(motor_a_backward_pin, GPIO.LOW)
    GPIO.output(motor_b_forward_pin, GPIO.LOW)
    GPIO.output(motor_b_backward_pin, GPIO.HIGH)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
host = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
port = 85     # Choose a port number for the communication
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
    
    # Process the received command and control the robot's movement
    if data == 'forward':
        print("Moving forward")
        move_forward()
    elif data == 'backward':
        print("Moving backward")
        move_backward()
    elif data == 'left':
        print("Turning left")
        turn_left()
    elif data == 'right':
        print("Turning right")
        turn_right()
    else:
        print("Invalid command")

    # Add a small delay to control the duration of the movement
    time.sleep(0.5)

# Clean up GPIO pins
GPIO.cleanup()

conn.close()
