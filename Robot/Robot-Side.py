#E.L.A.R.T Framework By: Nathan Aruna & Christos Velmachos
#Robot Side
import cv2
import threading
import struct
import pickle
import time
import os
import RPi.GPIO as GPIO
import subprocess
import socket
import glob
import serial

# ---------Contreller command handler ---------
def handle_controller_client(conn, addr):
    
    def motor_front():
        motor_pin_cleanup = [17, 18, 19, 27, 20, 12]
        
        GPIO.setmode(GPIO.BCM)
        motor1_pwm = 17  
        motor1_in1 = 18 
        motor1_in2 = 19  

        motor2_pwm = 27 
        motor2_in1 = 20  
        motor2_in2 = 12 
    # Motor 1
        GPIO.setup(motor1_pwm, GPIO.OUT)
        GPIO.setup(motor1_in1, GPIO.OUT)
        GPIO.setup(motor1_in2, GPIO.OUT)
    # Motor 2
        GPIO.setup(motor2_pwm, GPIO.OUT)
        GPIO.setup(motor2_in1, GPIO.OUT)
        GPIO.setup(motor2_in2, GPIO.OUT)
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
            time.sleep(0.3)
            
        finally:
            motor1_pwm_obj.stop()
            motor2_pwm_obj.stop()
            GPIO.cleanup(motor_pin_cleanup)   
            
    def motor_left():
        motor_pin_cleanup = [17, 18, 19, 27, 20, 12]
        
        GPIO.setmode(GPIO.BCM)
        motor1_pwm = 17  
        motor1_in1 = 18 
        motor1_in2 = 19  

        motor2_pwm = 27 
        motor2_in1 = 20  
        motor2_in2 = 12 
        
    # Motor 1
        GPIO.setup(motor1_pwm, GPIO.OUT)
        GPIO.setup(motor1_in1, GPIO.OUT)
        GPIO.setup(motor1_in2, GPIO.OUT)
    # Motor 2
        GPIO.setup(motor2_pwm, GPIO.OUT)
        GPIO.setup(motor2_in1, GPIO.OUT)
        GPIO.setup(motor2_in2, GPIO.OUT)
    
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
            set_motor_speed(motor2_pwm_obj, motor2_in1, motor2_in2, speed)
            time.sleep(0.3)
            
        finally:
            motor2_pwm_obj.stop()
            GPIO.cleanup(motor_pin_cleanup)
            
    def motor_right():
        motor_pin_cleanup = [17, 18, 19, 27, 20, 12]

        GPIO.setmode(GPIO.BCM)
        motor1_pwm = 17  
        motor1_in1 = 18 
        motor1_in2 = 19  

        motor2_pwm = 27 
        motor2_in1 = 20  
        motor2_in2 = 12 
        
    # Motor 1
        GPIO.setup(motor1_pwm, GPIO.OUT)
        GPIO.setup(motor1_in1, GPIO.OUT)
        GPIO.setup(motor1_in2, GPIO.OUT)
    # Motor 2
        GPIO.setup(motor2_pwm, GPIO.OUT)
        GPIO.setup(motor2_in1, GPIO.OUT)
        GPIO.setup(motor2_in2, GPIO.OUT)
    
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
            set_motor_speed(motor1_pwm_obj, motor1_in1, motor1_in2, -speed)
            set_motor_speed(motor2_pwm_obj, motor2_in1, motor2_in2, -speed)

            time.sleep(0.3)
            
        finally:
            motor1_pwm_obj.stop()
            GPIO.cleanup(motor_pin_cleanup)
        
    def motor_back():
        motor_pin_cleanup = [17, 18, 19, 27, 20, 12]

        GPIO.setmode(GPIO.BCM)

        motor1_pwm = 17  
        motor1_in1 = 18 
        motor1_in2 = 19  

        motor2_pwm = 27 
        motor2_in1 = 20  
        motor2_in2 = 12 
        
    # Motor 1
        GPIO.setup(motor1_pwm, GPIO.OUT)
        GPIO.setup(motor1_in1, GPIO.OUT)
        GPIO.setup(motor1_in2, GPIO.OUT)
    # Motor 2
        GPIO.setup(motor2_pwm, GPIO.OUT)
        GPIO.setup(motor2_in1, GPIO.OUT)
        GPIO.setup(motor2_in2, GPIO.OUT)
    
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
            set_motor_speed(motor1_pwm_obj, motor1_in1, motor1_in2, -speed)
            set_motor_speed(motor2_pwm_obj, motor2_in1, motor2_in2, speed)
            time.sleep(0.3)
            
        finally:
            motor1_pwm_obj.stop()
            motor2_pwm_obj.stop()
            GPIO.cleanup(motor_pin_cleanup)

    
    # Function to turn on/off navigation lights
    def navLightsOn():
        GPIO.setmode(GPIO.BCM)
        relayNav = 13
        GPIO.setup(relayNav, GPIO.OUT)
        GPIO.output(relayNav, GPIO.HIGH)
        
    def navLightsOff():
        GPIO.setmode(GPIO.BCM)
        relayNav = 13
        GPIO.setup(relayNav, GPIO.OUT)
        GPIO.output(relayNav, GPIO.LOW)
        
    # Function to turn on/off headlights
    def headlightsOff():
        GPIO.setmode(GPIO.BCM)
        relayNav = 21
        GPIO.setup(relayNav, GPIO.OUT)
        GPIO.output(relayNav, GPIO.HIGH)
        
    def headlightsOn():
        GPIO.setmode(GPIO.BCM)
        relayNav = 21
        GPIO.setup(relayNav, GPIO.OUT)
        GPIO.output(relayNav, GPIO.LOW)
        
        
    # Function to reboot the system
    def sysReboot():
        print('System Rebooting....')
        time.sleep(5) 
        os.system('sudo reboot')

    # Function to shutdown the system (robot side)
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
                    sysShutdown()
                
                elif data == 'front':
                    motor_front_thread = threading.Thread(target=motor_front)
                    motor_front_thread.start()
                    
                elif data == 'back':
                    motor_back_thread = threading.Thread(target=motor_back)
                    motor_back_thread.start()
                    
                elif data == 'left':
                    motor_left_thread = threading.Thread(target=motor_left)
                    motor_left_thread.start()
                
                elif data == 'right':
                    motor_right_thread = threading.Thread(target=motor_right)
                    motor_right_thread.start()
                    
                elif data == 'motortest':
                    motor_test_thread = threading.Thread(target=motor_front)
                    motor_test_thread.start()
                
                elif data == 'nav-on':
                    navLightsOn_thread = threading.Thread(target= navLightsOn)
                    navLightsOn_thread.start()
                  
                elif data == 'nav-off':
                    navLightsOff_thread = threading.Thread(target= navLightsOff)
                    navLightsOff_thread.start()
                    
                elif data == 'headlight-on':
                    headlightsOn_thread = threading.Thread(target= headlightsOn)
                    headlightsOn_thread.start()
                    
                elif data == 'headlight-off':
                    headlightsOff_thread = threading.Thread(target= headlightsOff)
                    headlightsOff_thread.start()
                    
                elif data == 'auto':
                    print("Auto Mode On")
                    
                elif data == 'overide':
                    print("Overide Mode On")
               
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()
        print("Client disconnected:", addr)


 #------------- getting the temp from the 1 wire file ---------        
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
        temperature_file = f'/sys/bus/w1/devices/{sensor_id}/w1_slave' 
               
        with open(temperature_file, 'r') as file:
            lines = file.readlines()

        if lines[0].strip()[-3:] == 'YES':
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
    try:
        while True:
            ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust port name and baud rate as needed
            line = ser.readline().decode('latin-1').strip()

            # Check if the line is not empty
            if line:
                # Splitting values into a list of key-value pairs using "|" as separator
                pairs = line.split("|")

                # Creating a dictionary from key-value pairs with special handling for GPS field
                sensor_data = {}
                for pair in pairs:
                    key_value = pair.split(":")
                    if len(key_value) == 2:
                        key, value = key_value
                        key, value = key.strip(), value.strip()
                        # Special handling for GPS field, don't convert to int
                        if key.lower() == 'gps':
                            sensor_data[key] = value
                        else:
                            try:
                                sensor_data[key] = int(value)
                            except ValueError:
                                print(f"Invalid value for key {key}: {value}")
                    else:
                        print(f"Invalid key-value pair: {pair}")

                print(sensor_data)
            else:
                print("Empty line received.")

            
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

          
            temperature_data = f"[CPU TEMP: {cpu_temperature:.2f} °C] [DS18B20 TEMP: {ds18b20_temperature:.2f} °C]" if ds18b20_temperature is not None else f"[CPU TEMP: {cpu_temperature:.2f} °C] [DS18B20 NOT FOUND]"

            # Send data to controller
            try:
                conn.sendall(temperature_data.encode())
            except (BrokenPipeError, ConnectionResetError):
                print("Sensor: Client disconnected.")
                break
            except Exception as send_error:
                print("Error sending data to controller:", send_error)
                break

            time.sleep(3)
    except Exception as e:
        print("Sensor connection error:", addr, e)
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

camera = cv2.VideoCapture(0)  

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
    