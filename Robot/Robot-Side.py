import cv2
import threading
import struct
import pickle
import time
import os
import RPi.GPIO as GPIO
import time
import subprocess
import socket

#speaker setup
GPIO.setmode(GPIO.BCM)
speaker_pin = 17
GPIO.setup(speaker_pin, GPIO.OUT)
pwm = GPIO.PWM(speaker_pin, 100)
relayNav = 21
GPIO.setup(relayNav, GPIO.OUT)


def play_startup_tone():
    pwm.start(70) 
    pwm.ChangeFrequency(1000)  
    time.sleep(0.5)
    pwm.ChangeFrequency(300)
    time.sleep(0.5)
    pwm.ChangeFrequency(1000)
    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()
    
def play_connection_tone():
    pwm.start(70) 
    pwm.ChangeFrequency(1000)  
    time.sleep(0.5)
    pwm.ChangeFrequency(300)
    time.sleep(0.5)
    pwm.ChangeFrequency(1000)
    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()
  

play_startup_tone()


# ---------Controller Client Command Receiver---------
def handle_controller_client(conn, addr):
    
    def navLightsOn():
        GPIO.output(relayNav, GPIO.HIGH)
        print("Turning On Navigation Lights")

    
    def navLightsOff():
        GPIO.output(relayNav, GPIO.LOW)
        print("Turning Off Navigation Lights")
    
    def motor_test():
        GPIO.setmode(GPIO.BCM)
        motor1_pwm = 17  
        motor1_in1 = 18 
        motor1_in2 = 19  

        motor2_pwm = 27 
        motor2_in1 = 20  
        motor2_in2 = 12 
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
            set_motor_speed(motor1_pwm_obj, motor1_in1, motor1_in2, speed)
            set_motor_speed(motor2_pwm_obj, motor2_in1, motor2_in2, -speed)
            time.sleep(1)
        finally:
            motor1_pwm_obj.stop()
            motor2_pwm_obj.stop()
            GPIO.cleanup()
            
    def motor_test_wrapper():
        motor_test()
        
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
        
#-------------Waiting for command from client---------        
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
              
                if data == 'reboot':
                    sysReboot()
                    
                elif data == 'shutdown':
                    sysShutdown()
                    
                elif data == 'motortest':
                    motor_test_thread = threading.Thread(target=motor_test_wrapper)
                    motor_test_thread.start()
                
                elif data == 'nav-on':
                    navLightsOn()
                    
                elif data == 'auto':
                    print("Auto Mode On")
                    
                elif data == 'overide':
                    print("Overide Mode On")
                    
                elif data == 'nav-off':
                    navLightsOff()
                    
                elif data == 'headlight1':
                    print("Turning On Headlights 1")
                    
                elif data == 'headlight2':
                    print("Turning On Headlights 2")
#-----------------------------------------------------
               
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()
        print("Client disconnected:", addr)
#-----------------------------------------------------




# ---------------Sensor Data Transmitter--------------
def handle_sensor_connection(conn, addr):
    try:
        while True:
            result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            temperature_str = result.stdout.strip()
            temperature = float(temperature_str.split('=')[1].replace("'C", ""))
            temperature_data = f"[CPU TEMP: {temperature:.2f} °C]"
            time.sleep(3)
            try:
                conn.sendall(temperature_data.encode())
            except (BrokenPipeError, ConnectionResetError):
                print("Sensor: Client disconnected.")
                break
    except:
        print("Sensor connection error:", addr)
    finally:
        conn.close()
#-----------------------------------------------------
     

camera = cv2.VideoCapture(0)  # Use 0 for the first camera device (change the index if needed)


#-------Set up a socket server for sesnor data--------
sensor_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_server_address = ('0.0.0.0', 86)  # Replace with your server's IP and port
sensor_server_socket.bind(sensor_server_address)
sensor_server_socket.listen()
#-----------------------------------------------------

#----Set up a socket server for controller client-----
controller_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller_server_address = ('0.0.0.0', 87)  # Replace with your server's IP and port
controller_server_socket.bind(controller_server_address)
controller_server_socket.listen()
#-----------------------------------------------------


print("Waiting For Controller Client Connection... ")
while True:

    sensor_conn, sensor_addr = sensor_server_socket.accept()
    print("Port 86: Connected", sensor_addr)
    sensor_thread = threading.Thread(target=handle_sensor_connection, args=(sensor_conn, sensor_addr))
    sensor_thread.start()


    controller_conn, controller_addr = controller_server_socket.accept()
    print("Port 87: Connected", controller_addr)
    controller_thread = threading.Thread(target=handle_controller_client, args=(controller_conn, controller_addr))
    controller_thread.start()
    play_startup_tone()
