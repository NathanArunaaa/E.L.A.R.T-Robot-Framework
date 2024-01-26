#E.L.A.R.T Robot Controller Interface By: Nathan Aruna

import socket
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from io import BytesIO
import struct
import datetime
import pickle
import random
import os
import math
import time
import queue
import keyboard


#----------------------List for commands---------------------
command_history = []

gui_queue = queue.Queue()

#--------------------Connect to the robot--------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.4.1', 87)  
client_socket.connect(server_address)



#----------------------Artificial Horizon--------------------
def calculate_horizon_coords(canvas_width, canvas_height, pitch, roll):
    horizon_length = 100  # You can adjust this length as needed
    pitch_radians = math.radians(pitch)
    roll_radians = math.radians(roll)

    # Calculate the coordinates of the two ends of the horizon line
    x1 = canvas_width / 2 - horizon_length * math.sin(roll_radians)
    y1 = canvas_height / 2 - horizon_length * math.cos(roll_radians) * math.sin(pitch_radians)
    x2 = canvas_width / 2 + horizon_length * math.sin(roll_radians)
    y2 = canvas_height / 2 + horizon_length * math.cos(roll_radians) * math.sin(pitch_radians)

    return x1, y1, x2, y2

def draw_artificial_horizon(canvas, pitch, roll):
    canvas.delete("horizon")

    # Get the canvas size
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Calculate the coordinates of the horizon line
    x1, y1, x2, y2 = calculate_horizon_coords(canvas_width, canvas_height, pitch, roll)

    # Draw the horizon line
    canvas.create_line(x1, y1, x2, y2, fill="white", tags="horizon", width=2, arrow=tk.BOTH)


#---------------------Receiving Sensor Data------------------
def update_sensor_data():
    try:
        sensor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sensor_client_socket.connect(('192.168.4.1', 86))

        while True:
            # Receive sensor data from the server
            sensor_data = sensor_client_socket.recv(1024).decode()

            # Extract GPS data
            if "[GPS:" in sensor_data:
                gps_start = sensor_data.find("[GPS:")
                gps_end = sensor_data.find("]", gps_start)
                gps_data = sensor_data[gps_start:gps_end + 1]

                # Update the label with the extracted location information
                location_info = f"Location: {gps_data}"
                location_label.config(text=location_info)
            else:
                gps_data = "[GPS: N/A]"

            # Extract other sensor data
            externalTempsensor = sensor_data[sensor_data.find("[Temp1:"):sensor_data.find("]", sensor_data.find("[Temp1:")) + 1]
            rpiTemp = sensor_data[sensor_data.find("[Temp2:"):sensor_data.find("]", sensor_data.find("[Temp2:")) + 1]

            # Update temperature labels with extracted data
            gui_queue.put(externalTempsensor)
            update_temperature_labels(externalTempsensor)

            gui_queue.put(rpiTemp)
            update_temperature_labels(rpiTemp)

            # Extract and print GPS data
            print("Received GPS data:", gps_data)

    except Exception as e:
        print("Error updating sensor data:", e)

    finally:
        sensor_client_socket.close()
        
def extract_cpu_temperature(sensor_data):
    try:
        cpu_temp_start = sensor_data.find("CPU TEMP:") + len("CPU TEMP: ")
        cpu_temp_end = sensor_data.find(" °C", cpu_temp_start)
        cpu_temperature = float(sensor_data[cpu_temp_start:cpu_temp_end])
        return cpu_temperature
    except ValueError:
        return None


# Updated extract_ds18b20_temperature function
def extract_ds18b20_temperature(sensor_data):
    try:
        ds18b20_temp_start = sensor_data.find("DS18B20 TEMP:") + len("DS18B20 TEMP: ")
        ds18b20_temp_end = sensor_data.find(" °C", ds18b20_temp_start)
        ds18b20_temperature = float(sensor_data[ds18b20_temp_start:ds18b20_temp_end])
        return ds18b20_temperature
    except ValueError:
        return None
                
def update_temperature_labels(sensor_data):
    cpu_temperature = extract_cpu_temperature(sensor_data)
    ds18b20_temperature = extract_ds18b20_temperature(sensor_data)

    if cpu_temperature is not None:
        cpu_temp_label.config(text=f"CPU Temperature: {cpu_temperature:.2f} °C")

    if ds18b20_temperature is not None:
        external_temp_label.config(text=f"External Temperature: {ds18b20_temperature:.2f} °C")
gui_queue = queue.Queue()
 
def update_gui():
    try:
        while True:
            rpiTemp = gui_queue.get_nowait()
            update_temperature_labels(rpiTemp)
    except queue.Empty:
        pass
    root.after(100, update_gui)

    
    
# -------------------Update Camera Feed----------------------
def update_camera_feed():
    try:
        while True:
            # Request camera frame from the server
            client_socket.sendall("camera_frame".encode())
            frame_size_data = client_socket.recv(4)
            if not frame_size_data:
                break
            frame_size = struct.unpack('!L', frame_size_data)[0]
            frame_data = b''
            while len(frame_data) < frame_size:
                data = client_socket.recv(frame_size - len(frame_data))
                if not data:
                    break
                frame_data += data

            if len(frame_data) == frame_size:
                frame = pickle.loads(frame_data)
                
                image = Image.fromarray(frame)
                image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                
                canvas.create_image(0, 0, anchor=tk.NW, image=image)
                canvas.image = image

                pitch = 30
                roll = 30

                # Update the canvas with the new pitch and roll angles
                draw_artificial_horizon(canvas, pitch, roll)

                canvas_width = canvas.winfo_width()
                angle_text = f"Pitch: {pitch:.2f}°\nRoll: {roll:.2f}°"
                canvas.create_text(10, 10, anchor=tk.NW, text=angle_text, fill="white", font=("Arial", 14))
                
                x_offset = 10  
                y_offset = 10  

                command_text = "\n".join(command_history[-5:])  # Show the last 5 commands
                canvas.create_text(canvas_width - x_offset, y_offset, anchor=tk.NE, text=command_text, fill="white", font=("Arial", 12))

    except Exception as e:
        print("Error updating camera feed:", e)



# -----------Function to send commands to the robot side-----------
def on_button_click(command):
    print(f"Sending command: {command}")
    client_socket.sendall(command.encode())

    command_history.append(command) 
    if len(command_history) > 10:
        command_history.pop(0)


def button_click_thread(command):
    thread = threading.Thread(target=on_button_click, args=(command,))
    thread.start()

def handle_key_press():
    while True:
        # Detect key presses using the keyboard library
        if keyboard.read_key() == "w":
            button_click_thread("move_forward_command")
            print("w")
        elif keyboard.is_pressed('a'):
            button_click_thread("left")  
            
        elif keyboard.is_pressed('s'):
            button_click_thread("back") 
             
        elif keyboard.is_pressed('d'):
            button_click_thread("turn_right_command")  # Replace with your actual turn right command

        time.sleep(0.1)  # Adjust the sleep time based on your requirements


# ---------Function to update the temp sensor data----------------

# ------------Function to update the date and time--------------
def update_time():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_label.config(text="Current Time: " + current_time)
    root.after(1000, update_time)  


    
# --------------Function to update the progress bar-------------
def update_progress_etlu():
    value = progress_var_etlu.get() + 10
    if value > 100:
        value = 0
    progress_var_etlu.set(value)
    root.after(1000, update_progress_etlu)
    
def update_progress_battery():
    value = progress_var_battery.get() + 10
    if value > 100:
        value = 0
    progress_var_battery.set(value)
    root.after(1000, update_progress_battery)


def shutdown_controller():
    quit()


#--------------------------Reboot Window------------------------
def confirm_reboot():
    smaller_window_reboot = tk.Toplevel(root, bg='#323232')
    smaller_window_reboot.title("E.L.A.R.T")
    smaller_window_reboot.geometry("200x100")  # Set the size of the new window

    label = tk.Label(smaller_window_reboot, fg='white', bg='#323232', text="CONFIRM REBOOT")
    label.pack()
    
    button_reboot_yes = tk.Button(smaller_window_reboot, fg='red', text="Yes", activebackground='tomato', command=lambda:  button_click_thread("reboot"))
    button_reboot_yes.pack()
    button_reboot_no = tk.Button(smaller_window_reboot, fg='green', text="No", activebackground='tomato', command=smaller_window_reboot.destroy)
    button_reboot_no.pack()


#--------------------------Shutdow Window-----------------------
def confirm_Shutdown():
    smaller_window_shutdown = tk.Toplevel(root, bg='#323232')
    smaller_window_shutdown.title("E.L.A.R.T ")
    smaller_window_shutdown.geometry("200x100")  # Set the size of the new window

    label = tk.Label(smaller_window_shutdown, bg='#323232', fg='white', text="CONFIRM SHUTDOWN")
    label.pack()
    
    button_shutdown_yes = tk.Button(smaller_window_shutdown, fg='red', text="Yes", activebackground='tomato', command=lambda:  button_click_thread("shutdown"))
    button_shutdown_yes.pack()
    button_shutdown_no = tk.Button(smaller_window_shutdown, fg='green', text="No", activebackground='tomato', command=smaller_window_shutdown.destroy)
    button_shutdown_no.pack()


#--------------------------Shutdown Controller Window-----------------------
def confirm_controller_Shutdown():
    smaller_window_shutdown = tk.Toplevel(root, bg='#323232')
    smaller_window_shutdown.title("E.L.A.R.T ")
    smaller_window_shutdown.geometry("250x100")  # Set the size of the new window

    label = tk.Label(smaller_window_shutdown,  bg='#323232', fg='white', text="CONFIRM CONRTOLLER SHUTDOWN")
    label.pack()
    
    button_shutdown_yes = tk.Button(smaller_window_shutdown, fg='red', text="Yes", activebackground='tomato', command=shutdown_controller)
    button_shutdown_yes.pack()
    button_shutdown_no = tk.Button(smaller_window_shutdown, fg='green', text="No", activebackground='tomato', command=smaller_window_shutdown.destroy)
    button_shutdown_no.pack()


#--------------------------Sensor Window------------------------
def sensor_window():
    sensor_readings = tk.Toplevel(root, bg='#323232')
    sensor_readings.title("E.L.A.R.T Sensors")
    sensor_readings.geometry("350x250")  

    label = tk.Label(sensor_readings, bg='#323232', fg='white', text="SENSOR READINGS")
    label.pack()

    progress_var_etlu = tk.DoubleVar(sensor_readings)
    vertical_progress = ttk.Progressbar(sensor_readings, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
    vertical_progress.pack(side=tk.LEFT, padx=30)

    progress_var_etlu = tk.DoubleVar(sensor_readings)
    vertical_progress = ttk.Progressbar(sensor_readings, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
    vertical_progress.pack(side=tk.LEFT, padx=30)

    progress_var_etlu = tk.DoubleVar(sensor_readings)
    vertical_progress = ttk.Progressbar(sensor_readings, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
    vertical_progress.pack(side=tk.LEFT, padx=30)
    
    progress_var_etlu = tk.DoubleVar(sensor_readings)
    vertical_progress = ttk.Progressbar(sensor_readings, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
    vertical_progress.pack(side=tk.LEFT, padx=30)
   
    
    
root = tk.Tk()
root.title("E.L.A.R.T - Controller")

root.config(bg='#323232')

#----------------------------------
sensor_frame = tk.Frame(root)
sensor_frame.pack(side=tk.TOP, pady=10)
sensor_frame.config(bg='#323232')

   
# ---------------------Temperature Lables------------------------

cpu_temp_label = tk.Label(sensor_frame, bg='#323232', fg='red', text="[Temp2: N/A]")
cpu_temp_label.pack()

external_temp_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Temp2: N/A]")
external_temp_label.pack(side=tk.LEFT)

Temp2_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Temp2: N/A]")
Temp2_label.pack(side=tk.LEFT)

Temp3_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Temp3: N/A]")
Temp3_label.pack(side=tk.LEFT)


time_label = tk.Label(sensor_frame,bg='#323232',  fg='gray', text="Current Time: ")
time_label.pack(side=tk.LEFT, pady=10)

#------------------------Sensor Lables--------------------------
location_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Sens1: N/A]")
location_label.pack(side=tk.LEFT)

Temp2_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Sens2: N/A]")
Temp2_label.pack(side=tk.LEFT)

Temp3_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Sens3: N/A]")
Temp3_label.pack(side=tk.LEFT)


#----------------------Left Row Buttons-------------------------
current_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_directory, "assets", "logo-no-background.png")
image = Image.open(image_path)
image = image.resize((95, 60))  
photo = ImageTk.PhotoImage(image)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT)
left_frame.config(bg='#323232')

image_label = tk.Label(left_frame, bg='#323232', image=photo)
image_label.pack(side=tk.TOP,  padx=5, pady=5)


button_shutdown = tk.Button(left_frame, bg='#323232', fg='red', text="SHUTDOWN", activebackground='tomato', command=confirm_Shutdown)
button_shutdown.pack(side=tk.TOP, padx=5, pady=5)

button_reboot = tk.Button(left_frame,  bg='#323232', fg='red', text="  REBOOT  ", command=confirm_reboot)
button_reboot.pack(side=tk.TOP, padx=5, pady=0)

divider = tk.Label(left_frame,  bg='#323232', text="-----------------------", font=("Helvetica", 12),  fg='grey')
divider.pack()

button_nav1 = tk.Button(left_frame,  bg='#323232',  fg='blue', text="   NAV-ON   ", command=lambda:  button_click_thread("nav-off"))
button_nav1.pack(side=tk.TOP, padx=5, pady=0)

button_headlight1 = tk.Button(left_frame, bg='#323232',  fg='blue', text="HEADLIGHT1", command=lambda:  button_click_thread("headlight1"))
button_headlight1.pack(side=tk.TOP, padx=5, pady=0)

divider = tk.Label(left_frame,  bg='#323232', text="-----------------------", font=("Helvetica", 12), fg='grey', )
divider.pack()

button_console = tk.Button(left_frame, bg='#323232',  fg='green', text="SENSORS", command=sensor_window)
button_console.pack(side=tk.TOP, padx=5, pady=0)


progress_var_etlu = tk.DoubleVar(left_frame)
vertical_progress = ttk.Progressbar(left_frame,  orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
vertical_progress.pack(pady=10)

etlu = tk.Label(left_frame,  bg='#323232', fg='white', text="ETLU")
etlu.pack(side=tk.TOP, padx=5, pady=5)

etlu_warning = tk.Label(left_frame,  bg='#323232', fg='Green', text="Evironment Is Safe")
etlu_warning.pack(side=tk.TOP, padx=5, pady=5)


#----------------------------Camera------------------------------
canvas = tk.Canvas(root, width=1180, height=790)
canvas.pack(side=tk.LEFT)


#----------------------Right Row Buttons-------------------------
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT)
right_frame.config(bg='#323232')


git_version_label = tk.Label(right_frame, fg='white',  bg='#323232', text="Stable Version 2.87.1 (Controller Client)", font=("Helvetica", 12), wraplength=85)
git_version_label.pack(padx=20, pady=10)

close_controller = tk.Button(right_frame , bg='#323232', fg='red',text="C-SHUTDOWN", command=confirm_controller_Shutdown)
close_controller.pack(side=tk.TOP, padx=5, pady=5)

button_overide = tk.Button(right_frame, bg='#323232', fg='red',text="OVERIDE", command=lambda: button_click_thread("overide"))
button_overide.pack(side=tk.TOP, padx=5, pady=5)


divider = tk.Label(right_frame, bg='#323232', text="-----------------------", font=("Helvetica", 12), fg='grey')
divider.pack()


button_nav2 = tk.Button(right_frame, bg='#323232', fg='blue', text="  NAV-OFF  ", command=lambda:  button_click_thread("nav-on"))
button_nav2.pack(side=tk.TOP, padx=5, pady=0)

button_headlight2 = tk.Button(right_frame, bg='#323232', fg='blue', text="HEADLIGHT2", command=lambda:  button_click_thread("headlight2"))
button_headlight2.pack(side=tk.TOP, padx=5, pady=0)

divider = tk.Label(right_frame, bg='#323232', text="-----------------------", font=("Helvetica", 12), fg='grey')
divider.pack()


button_motortest = tk.Button(right_frame, bg='#323232', fg='green', text="MOTORTEST", command=lambda:  button_click_thread("motortest"))
button_motortest.pack(side=tk.TOP, padx=5, pady=5)

button_auto = tk.Button(right_frame, bg='#323232', fg='green', text="AUTO", command=lambda: button_click_thread("auto"))
button_auto.pack(side=tk.TOP, padx=5, pady=5)

progress_var_battery = tk.DoubleVar(right_frame)
vertical_progress = ttk.Progressbar(right_frame, orient='vertical', variable=progress_var_battery, length=200, mode='determinate')
vertical_progress.pack(pady=10)

battery_level = tk.Label(right_frame, bg='#323232', fg='white', text="Battery Level")
battery_level.pack(side=tk.TOP, padx=5, pady=5)


battery_value = tk.Label(right_frame,bg='#323232',  fg='white', text=progress_var_battery)
battery_value.pack(side=tk.TOP)


# ---------Function to start the Sensor + camera thread---------
def start_sensor_thread():
    update_thread = threading.Thread(target=update_sensor_data)
    update_thread.daemon = True
    update_thread.start()


def start_camera_thread():
    camera_thread = threading.Thread(target=update_camera_feed)
    camera_thread.daemon = True
    camera_thread.start()


key_press_thread = threading.Thread(target=handle_key_press)
key_press_thread.daemon = True
key_press_thread.start()

start_sensor_thread()
update_time()
start_camera_thread()
update_gui()

root.mainloop()
