import socket
import cv2
import threading
import struct
import pickle
import time
import os
import RPi.GPIO as GPIO
import time
import subprocess

# Function to handle sensor data
def handle_sensor_connection(conn, addr):
    try:
        while True:
            result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            temperature_str = result.stdout.strip()
            temperature = float(temperature_str.split('=')[1].replace("'C", ""))
            temperature_data = f"Sensor data: {temperature:.2f} °C"
            try:
                conn.sendall(temperature_data.encode())
            except (BrokenPipeError, ConnectionResetError):
                print("Sensor Script: Client disconnected.")
                break
    except:
        print("Sensor connection error:", addr)
    finally:
        conn.close()

# Function to handle movement control
def handle_controller_clinet(conn, addr):
    
    def motor_test():
    # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

    # Define motor control pins for Motor 1
        motor1_pwm = 17  # Example GPIO pin for Motor 1 PWM
        motor1_in1 = 18  # Example GPIO pin for Motor 1 IN1
        motor1_in2 = 19  # Example GPIO pin for Motor 1 IN2

    # Define motor control pins for Motor 2
        motor2_pwm = 27  # Example GPIO pin for Motor 2 PWM
        motor2_in1 = 20  # Example GPIO pin for Motor 2 IN1
        motor2_in2 = 12  # Example GPIO pin for Motor 2 IN2

    # Set up pins as output for Motor 1
        GPIO.setup(motor1_pwm, GPIO.OUT)
        GPIO.setup(motor1_in1, GPIO.OUT)
        GPIO.setup(motor1_in2, GPIO.OUT)

    # Set up pins as output for Motor 2
        GPIO.setup(motor2_pwm, GPIO.OUT)
        GPIO.setup(motor2_in1, GPIO.OUT)
        GPIO.setup(motor2_in2, GPIO.OUT)

    # Set up PWM for both motors
        motor1_pwm_obj = GPIO.PWM(motor1_pwm, 1000)  # Frequency: 1000 Hz
        motor2_pwm_obj = GPIO.PWM(motor2_pwm, 1000)
        motor1_pwm_obj.start(0)  # Start PWM with 0% duty cycle
        motor2_pwm_obj.start(0)
 
    # Function to set motor speed
        def set_motor_speed(pwm_obj, in1, in2, speed):
            if speed >= 0:
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
            else:
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
            pwm_obj.ChangeDutyCycle(abs(speed))

        try:
            speed = 100  # Set the speed as a percentage (-100 to 100)
            print("at try stage")
            set_motor_speed(motor1_pwm_obj, motor1_in1, motor1_in2, speed)
            set_motor_speed(motor2_pwm_obj, motor2_in1, motor2_in2, -speed)
        
        # Allow motors to run for 5 seconds
            time.sleep(5)
        
        finally:
        # Stop PWM and cleanup
            motor1_pwm_obj.stop()
            motor2_pwm_obj.stop()
            GPIO.cleanup()
        
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
        os.system('sudo shutdown -h now')
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
                    
                elif data == 'motortest':
                    motor_test()
                
                elif data == 'nav1':
                    print("Turning On Navigation Lights 1")
                    
                elif data == 'auto':
                    print("Auto Mode On")
                    
                elif data == 'overide':
                    #add logic to turn on overide mode
                    print("Overide Mode On")
                    
                elif data == 'nav2':
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
        
camera = cv2.VideoCapture(0)  # Use 0 for the first camera device (change the index if needed)


# Set up a socket server for sensor data
sensor_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_server_address = ('0.0.0.0', 86)  # Replace with your server's IP and port
sensor_server_socket.bind(sensor_server_address)
sensor_server_socket.listen()

# Set up a socket server for movement control
movement_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
movement_server_address = ('0.0.0.0', 87)  # Replace with your server's IP and port
movement_server_socket.bind(movement_server_address)
movement_server_socket.listen()

print("Central Controller: Waiting for sensor connection...")
while True:
    sensor_conn, sensor_addr = sensor_server_socket.accept()
    print("Central Controller: Sensor connected:", sensor_addr)
    sensor_thread = threading.Thread(target=handle_sensor_connection, args=(sensor_conn, sensor_addr))
    sensor_thread.start()

    movement_conn, movement_addr = movement_server_socket.accept()
    print("Central Controller: Movement connected:", movement_addr)
    movement_thread = threading.Thread(target=handle_controller_clinet, args=(movement_conn, movement_addr))
    movement_thread.start()

