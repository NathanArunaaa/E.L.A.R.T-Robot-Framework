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
import glob
import pynmea2
import serial

# ---------Contreller command handler ---------
def handle_controller_client(conn, addr):
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




def find_sensor_id():
    try:
        sensor_folder = glob.glob('/sys/bus/w1/devices/28*')[0]
        sensor_id = os.path.basename(sensor_folder)
        return sensor_id
    except IndexError:
        print("DS18B20 sensor not found.")
        return None

def read_temperature(sensor_id):
    try:
        # Path to the temperature file
        temperature_file = f'/sys/bus/w1/devices/{sensor_id}/w1_slave'
        
        # Read the raw temperature data
        with open(temperature_file, 'r') as file:
            lines = file.readlines()

        # Check if the CRC is valid
        if lines[0].strip()[-3:] == 'YES':
            # Extract the temperature from the second line
            temperature_str = lines[1].split('=')[1]
            temperature_celsius = float(temperature_str) / 1000.0

            return temperature_celsius
        else:
            return None

    except Exception as e:
        print(f"Error reading temperature: {str(e)}")
        return None

# ---------------Sensor Data Transmitter--------------
def handle_sensor_connection(conn, addr):
    # Open the serial port for the GPS module
    gps_serial = serial.Serial("/dev/ttyS0", 9600, timeout=5.0)

    try:
        while True:
            # Read GPS data
            gps_data = gps_serial.readline().decode('utf-8')

            # Parse GPS data
            if gps_data.startswith('$GPGGA'):
                try:
                    gps_msg = pynmea2.parse(gps_data)
                    latitude = gps_msg.latitude
                    longitude = gps_msg.longitude
                    gps_location = f"[GPS: Lat {latitude}, Lon {longitude}]"
                except pynmea2.ParseError as e:
                    gps_location = "[GPS: Parsing Error]"
            else:
                gps_location = "[GPS: No Fix]"

            # Get CPU temperature
            result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            cpu_temperature_str = result.stdout.strip()
            cpu_temperature = float(cpu_temperature_str.split('=')[1].replace("'C", ""))

            # Read DS18B20 temperature
            ds18b20_sensor_id = find_sensor_id()
            if ds18b20_sensor_id:
                ds18b20_temperature = read_temperature(ds18b20_sensor_id)
            else:
                ds18b20_temperature = None

            # Format all sensor data
            sensor_data = f"{gps_location} [CPU TEMP: {cpu_temperature:.2f} °C] [DS18B20 TEMP: {ds18b20_temperature:.2f} °C]" if ds18b20_temperature is not None else f"{gps_location} [CPU TEMP: {cpu_temperature:.2f} °C] [DS18B20 NOT FOUND]"

            # Send data to controller
            try:
                conn.sendall(sensor_data.encode())
            except (BrokenPipeError, ConnectionResetError):
                print("Sensor: Client disconnected.")
                break

            time.sleep(3)  # Adjust delay as needed

    except Exception as e:
        print("Sensor connection error:", addr, e)
    finally:
        gps_serial.close()
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
    
