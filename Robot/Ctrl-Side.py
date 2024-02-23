#E.L.A.R.T Framework By: Nathan Aruna & Christos Velmachos
#Controller side

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
import queue
import keyboard
from pynput import keyboard
import tkintermapview

#----------------------List for commands---------------------
command_history = []

gui_queue = queue.Queue()

#--------------------Connect to the robot--------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.4.1', 87)  
client_socket.connect(server_address)





#---------------------Receiving Sensor Data------------------
def update_sensor_data():
    try:
       sensor_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sensor_client_socket.connect(('192.168.4.1', 86))  

       while True:
            externalTempsensor = sensor_client_socket.recv(240).decode()
            gui_queue.put(externalTempsensor)
            update_temperature_labels(externalTempsensor)
            
            rpiTemp = sensor_client_socket.recv(240).decode()
            gui_queue.put(rpiTemp)
            update_temperature_labels(rpiTemp)
            
            rpiTemp = sensor_client_socket.recv(240).decode()
            gui_queue.put(rpiTemp)
            update_temperature_labels(rpiTemp)


            
    except Exception as e:
        print("Error updating sensor data:", e)

    finally:
        sensor_client_socket.close()
        
def extract_temperature_data(sensor_data):
    try:
        start_index = sensor_data.find("Value:") + len("Value: ")
        data_str = sensor_data[start_index:]
        sensor_values = data_str.split(", ")

        extracted_values = {}
        for value in sensor_values:
            if ':' in value:
                key, val = value.split(":")
                extracted_values[key] = int(val)

        return extracted_values
    except ValueError:
        return None

# Updated extract_cpu_temperature function
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
    temperature_data = extract_temperature_data(sensor_data)
    cpu_temperature = extract_cpu_temperature(sensor_data)
    ds18b20_temperature = extract_ds18b20_temperature(sensor_data)
    latitude = temperature_data.get("LATITUDE", None)
    longitude = temperature_data.get("LONGITUDE", None)

    if cpu_temperature is not None:
        cpu_temp_label.config(text=f"CPU Temperature: {cpu_temperature:.2f} °C")

    if ds18b20_temperature is not None:
        external_temp_label.config(text=f"External Temperature: {ds18b20_temperature:.2f} °C")

    if latitude is not None and longitude is not None:
        gps_label.config(text=f"GPS: Lat {latitude:.6f}, Lon {longitude:.6f}")

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
                photo_image = ImageTk.PhotoImage(image)

    # Create or update the canvas image
                if hasattr(canvas, 'canvas_image'):
                  canvas.itemconfig(canvas.canvas_image, image=photo_image)
                else:
                  canvas.canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

    # Store the PhotoImage object in a custom attribute
                canvas.photo_image = photo_image

                

                canvas_width = canvas.winfo_width()

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

def on_key_press(key):
    try:
        if key.char == 'w':
            button_click_thread('front')
            print("Moving Forward")
        if key.char == 's':
            button_click_thread('back')
            print("Moving Backwards")
        if key.char == 'a':
            button_click_thread('left')
            print("Moving Left")
        if key.char == 'd':
            button_click_thread('right')
            print("Moving Right")
    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.esc:
            print("Escape key is pressed")

def listen_for_keys():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


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
    sensor_readings.geometry(f"{1000}x{700}")
    progress_var_etlu = tk.DoubleVar(sensor_readings)
    
    label = tk.Label(sensor_readings,  bg='#323232', fg='white', text="CONFIRM CONRTOLLER SHUTDOWN")
    label.pack()
    label = tk.Label(sensor_readings,  bg='#323232', fg='white', text="CONFIRM CONRTOLLER SHUTDOWN")
    label.pack()
    label = tk.Label(sensor_readings,  bg='#323232', fg='white', text="CONFIRM CONRTOLLER SHUTDOWN")
    label.pack()
    vertical_progress = ttk.Progressbar(sensor_readings, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
    vertical_progress.pack(side=tk.LEFT, padx=30)
    
    

    
    
def map_window():
    sensor_readings = tk.Toplevel(root, bg='#323232')
    sensor_readings.title("E.L.A.R.T Sensors")
    sensor_readings.geometry(f"{1000}x{700}")

    script_directory = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_directory, "elart.db")

    # Create map widget and use the tiles from the database
    map_widget = tkintermapview.TkinterMapView(sensor_readings, width=1000, height=700, corner_radius=0, use_database_only=True, max_zoom=17, database_path=database_path)
    map_widget.pack(fill="both", expand=True)

    # Set the tile server to the local database
    map_widget.set_tile_server("file://{}/elart.db".format(script_directory))

    # Set the address or location
    map_widget.set_address("nyc")
  
    
root = tk.Tk()
root.title("E.L.A.R.T - Controller")

root.config(bg='#323232')

#----------------------------------
sensor_frame = tk.Frame(root)
sensor_frame.pack(side=tk.TOP, pady=10)
sensor_frame.config(bg='#323232')

   
# ---------------------Temperature Lables------------------------

cpu_temp_label = tk.Label(sensor_frame, bg='#323232', fg='red', text="[CPU Temp: N/A]")
cpu_temp_label.pack()

external_temp_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Temp: N/A]")
external_temp_label.pack(side=tk.LEFT)

gps_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[GPS: N/A]")
gps_label.pack(side=tk.LEFT)

Temp3_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Temp3: N/A]")
Temp3_label.pack(side=tk.LEFT)


time_label = tk.Label(sensor_frame,bg='#323232',  fg='gray', text="Current Time: ")
time_label.pack(side=tk.LEFT, pady=10)

#------------------------Sensor Lables--------------------------
Temp1_label = tk.Label(sensor_frame, bg='#323232', fg='white', text="[Sens1: N/A]")
Temp1_label.pack(side=tk.LEFT)

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

button_headlight1 = tk.Button(left_frame, bg='#323232',  fg='blue', text="HEADLIGHT-ON", command=lambda:  button_click_thread("headlight-on"))
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
git_version_label.pack(padx=30, pady=10)

close_controller = tk.Button(right_frame , bg='#323232', fg='red',text="C-SHUTDOWN", command=confirm_controller_Shutdown)
close_controller.pack(side=tk.TOP, padx=5, pady=5)

button_overide = tk.Button(right_frame, bg='#323232', fg='red',text="OVERIDE", command=lambda: button_click_thread("overide"))
button_overide.pack(side=tk.TOP, padx=5, pady=5)


divider = tk.Label(right_frame, bg='#323232', text="-----------------------", font=("Helvetica", 12), fg='grey')
divider.pack()


button_nav2 = tk.Button(right_frame, bg='#323232', fg='blue', text="  NAV-OFF  ", command=lambda:  button_click_thread("nav-on"))
button_nav2.pack(side=tk.TOP, padx=5, pady=0)

button_headlight2 = tk.Button(right_frame, bg='#323232', fg='blue', text="  HEADLIGHT-OFF  ", command=lambda:  button_click_thread("headlight-off"))
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

def start_input_thread():
    key_listener_thread = threading.Thread(target=listen_for_keys)
    key_listener_thread.daemon = True
    key_listener_thread.start()

    # Your main application code goes here




start_input_thread()
start_sensor_thread()
update_time()
start_camera_thread()
update_gui()

root.mainloop()