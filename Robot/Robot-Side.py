#E.L.A.R.T Framework By: Nathan Aruna & Christos Velmachos
#Robot Side
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



# ---------Contreller command handler ---------
def handle_controller_client(conn, addr):
    
    #speaker setup
    
  
    # Function to test the motors
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
        motor1_pwm_obj = GPIO.PWM(motor1_pwm, 1000)  
        motor2_pwm_obj = GPIO.PWM(motor2_pwm, 1000)
        motor1_pwm_obj.start(0) 
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
            time.sleep(0.5)
            
        finally:
            motor1_pwm_obj.stop()
            motor2_pwm_obj.stop()
            GPIO.cleanup()
            
    
    # Function to turn on navigation lights
    def navLightsOn():
        GPIO.setmode(GPIO.BCM)
        relayNav = 13
        GPIO.setup(relayNav, GPIO.OUT)
        GPIO.output(relayNav, GPIO.HIGH)

    # Function to turn off navigation lights
    def navLightsOff():
        GPIO.setmode(GPIO.BCM)
        relayNav = 13
        GPIO.setup(relayNav, GPIO.OUT)
        GPIO.output(relayNav, GPIO.LOW)
        
    # Function to reboot the system
    def sysReboot():
        print('System Rebooting....')
        time.sleep(5) 
        os.system('sudo reboot')

    # Function to shutdown the system(robot side)
    def sysShutdown():
        print('System Shutdown....')
        time.sleep(5)
        os.system('sudo shutdown -h now')
        print("Client connected:", addr)
        
    # Function to send video frames to the controller client   
    def send_frame(conn, frame):
        frame_data = pickle.dumps(frame)
        frame_size = struct.pack('!L', len(frame_data))
        conn.sendall(frame_size + frame_data)

       
 #------------- looking for commands from controller client ---------        
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
              
                if data == 'reboot':
                    sysReboot()
                    
                elif data == 'shutdown':
                    motor_test_thread = threading.Thread(target=motor_test)
                    motor_test_thread.start()
                
                elif data == 'front':
                    motor_test_thread = threading.Thread(target=motor_test)
                    motor_test_thread.start()
                    
                elif data == 'back':
                    motor_test_thread = threading.Thread(target=motor_test)
                    motor_test_thread.start()
                    
                elif data == 'left':
                    motor_test_thread = threading.Thread(target=motor_test)
                    motor_test_thread.start()
                
                elif data == 'right':
                    motor_test_thread = threading.Thread(target=motor_test)
                    motor_test_thread.start()
                    
                elif data == 'motortest':
                    motor_test_thread = threading.Thread(target=motor_test)
                    motor_test_thread.start()
                
                elif data == 'nav-on':
                    navLightsOn_thread = threading.Thread(target= navLightsOn)
                    navLightsOn_thread.start()
                  
                elif data == 'auto':
                    print("Auto Mode On")
                    
                elif data == 'overide':
                    print("Overide Mode On")
                    
                elif data == 'nav-off':
                    navLightsOff_thread = threading.Thread(target= navLightsOff)
                    navLightsOff_thread.start()
                    
                elif data == 'headlight1':
                    print("Turning On Headlights 1")
                    
                elif data == 'headlight2':
                    print("Turning On Headlights 2")
               
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()
        print("Client disconnected:", addr)





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
    except:  # noqa: E722
        print("Sensor connection error:", addr)
    finally:
        conn.close()
     

camera = cv2.VideoCapture(0)  # Use 0 for the first camera device (change the index if needed)

#-------Set up a socket server for sesnor data--------
sensor_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_server_address = ('0.0.0.0', 86)  
sensor_server_socket.bind(sensor_server_address)
sensor_server_socket.listen()



#----Set up a socket server for controller client-----
controller_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller_server_address = ('0.0.0.0', 87) 
controller_server_socket.bind(controller_server_address)
controller_server_socket.listen()


print("Waiting For Controller Client Connection... ")

#---------connect both sides to transmit data and start threads-------
while True:

    sensor_conn, sensor_addr = sensor_server_socket.accept()
    print("Port 86: Connected", sensor_addr)
    sensor_thread = threading.Thread(target=handle_sensor_connection, args=(sensor_conn, sensor_addr))
    sensor_thread.start()


    controller_conn, controller_addr = controller_server_socket.accept()
    print("Port 87: Connected", controller_addr)
    controller_thread = threading.Thread(target=handle_controller_client, args=(controller_conn, controller_addr))
    controller_thread.start()
    
