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
import math


def get_pitch_angle():
    return random.uniform(-30, 30)  # Replace this with your actual pitch angle retrieval logic

# Sample function to get the roll angle (random for testing purposes)
def get_roll_angle():
    return random.uniform(100, 150)

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


# Function to update the camera feed
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
                # Convert the received bytes to a NumPy array
                frame = pickle.loads(frame_data)

                # Convert the NumPy array to an ImageTk object
                image = Image.fromarray(frame)

                # Resize the image to fit the canvas
                image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)

                # Convert the resized image to an ImageTk object
                image = ImageTk.PhotoImage(image)

                # Update the canvas with the new image
                canvas.create_image(0, 0, anchor=tk.NW, image=image)
                canvas.image = image

                # Get the pitch and roll angles (replace this with your actual angle calculation)
                pitch = get_pitch_angle()
                roll = get_roll_angle()

                # Update the canvas with the new pitch and roll angles
                draw_artificial_horizon(canvas, pitch, roll)

                angle_text = f"Pitch: {pitch:.2f}°\nRoll: {roll:.2f}°"
                canvas.create_text(10, 10, anchor=tk.NW, text=angle_text, fill="white", font=("Arial", 14))

    except Exception as e:
        print("Error updating camera feed:", e)




# ----------Function to start the camera feed thread----------
def start_camera_thread():
    camera_thread = threading.Thread(target=update_camera_feed)
    camera_thread.daemon = True
    camera_thread.start()
#---------------------------------------------------------------



# -----------Function to send commands to the server-----------
def on_button_click(command):
    print(f"Sending command: {command}")
    client_socket.sendall(command.encode())
#---------------------------------------------------------------



# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 87)  
client_socket.connect(server_address)


# ---------Function to update the temp sensor data----------------
def update_Temp1_data():
    # Replace this with actual sensor data retrieval logic
    sensor_reading = "Sensor Data: 123.45"
    Temp1_label.config(text=sensor_reading)
    root.after(1000, update_Temp1_data)  # Update the data every 1000ms (1 second)

def update_Temp2_data():
    sensor_reading = "Sensor Data: 123.45"
    Temp1_label.config(text=sensor_reading)
    root.after(1000, update_Temp2_data)  
    
def update_Temp3_data():
    sensor_reading = "Sensor Data: 123.45"
    Temp1_label.config(text=sensor_reading)
    root.after(1000, update_Temp3_data)  

#---------------------------------------------------------------   



# ------------Function to update the date and time--------------
def update_time():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_label.config(text="Current Time: " + current_time)
    root.after(1000, update_time)  # Update the time every 1000ms (1 second)
#---------------------------------------------------------------

    
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
#---------------------------------------------------------------  


def console_window():
    smaller_window = tk.Toplevel(root)
    smaller_window.title("E.L.A.R.TConsole Window")
    smaller_window.geometry("300x200")  # Set the size of the new window

    # Add widgets to the smaller window
    label = tk.Label(smaller_window, text="This is a smaller window.")
    label.pack()


root = tk.Tk()
root.title("E.L.A.R.T - Controller")


sensor_frame = tk.Frame(root)
sensor_frame.pack(side=tk.TOP, pady=10)
   
# ---------------------Temperature Lables------------------------
Temp1_label = tk.Label(sensor_frame, fg='white', text="[Temp1: N/A]")
Temp1_label.pack(side=tk.LEFT)

Temp2_label = tk.Label(sensor_frame, fg='white', text="[Temp2: N/A]")
Temp2_label.pack(side=tk.LEFT)

Temp3_label = tk.Label(sensor_frame, fg='white', text="[Temp3: N/A]")
Temp3_label.pack(side=tk.LEFT)
#---------------------------------------------------------------

time_label = tk.Label(sensor_frame, fg='gray', text="Current Time: ")
time_label.pack(side=tk.LEFT, pady=10)

#------------------------Sensor Lables--------------------------
Temp1_label = tk.Label(sensor_frame, fg='white', text="[Sens1: N/A]")
Temp1_label.pack(side=tk.LEFT)

Temp2_label = tk.Label(sensor_frame, fg='white', text="[Sens2: N/A]")
Temp2_label.pack(side=tk.LEFT)

Temp3_label = tk.Label(sensor_frame, fg='white', text="[Sens3: N/A]")
Temp3_label.pack(side=tk.LEFT)
#---------------------------------------------------------------





#----------------------Left Row Buttons-------------------------
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT)

Text1_label = tk.Label(left_frame, fg='white', text="E.L.A.R.T")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)

button_shutdown = tk.Button(left_frame, fg='red', text="SHUTDOWN", activebackground='tomato', command=lambda: on_button_click("shutdown"))
button_shutdown.pack(side=tk.TOP, padx=5, pady=5)

button_reboot = tk.Button(left_frame, fg='red', text="  REBOOT  ", command=lambda: on_button_click("reboot"))
button_reboot.pack(side=tk.TOP, padx=5, pady=5)

button_nav1 = tk.Button(left_frame,  fg='blue', text="   NAV-1   ", command=lambda: on_button_click("nav1"))
button_nav1.pack(side=tk.TOP, padx=5, pady=5)

button_headlight1 = tk.Button(left_frame, fg='blue', text="HEADLIGHT1", command=lambda: on_button_click("headlight1"))
button_headlight1.pack(side=tk.TOP, padx=5, pady=5)

button_console = tk.Button(left_frame, fg='blue', text="CONSOLE", command=console_window)
button_console.pack(side=tk.TOP, padx=5, pady=5)


progress_var_etlu = tk.DoubleVar(left_frame)
vertical_progress = ttk.Progressbar(left_frame, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
vertical_progress.pack(pady=10)

Text1_label = tk.Label(left_frame, fg='white', text="ETLU")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)
#----------------------------------------------------------------



#----------------------------Camera------------------------------

canvas = tk.Canvas(root, width=1180, height=790)
canvas.pack(side=tk.LEFT)

#---------------------------------------------------------------



#----------------------Right Row Buttons-------------------------
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT)

git_version_label = tk.Label(right_frame, text="Stable Version 2.87.1 (Controller Client)", font=("Helvetica", 12), wraplength=85)
git_version_label.pack(padx=20, pady=10)


button_overide = tk.Button(right_frame, fg='red',text="OVERIDE", command=lambda: on_button_click("overide"))
button_overide.pack(side=tk.TOP, padx=5, pady=5)

button_auto = tk.Button(right_frame, fg='green', text="AUTO", command=lambda: on_button_click("auto"))
button_auto.pack(side=tk.TOP, padx=5, pady=5)

button_nav2 = tk.Button(right_frame, fg='blue', text="  NAV-2  ", command=lambda: on_button_click("nav2"))
button_nav2.pack(side=tk.TOP, padx=5, pady=5)

button_headlight2 = tk.Button(right_frame, fg='blue', text="HEADLIGHT2", command=lambda: on_button_click("headlight2"))
button_headlight2.pack(side=tk.TOP, padx=5, pady=5)

progress_var_battery = tk.DoubleVar(right_frame)
vertical_progress = ttk.Progressbar(right_frame, orient='vertical', variable=progress_var_battery, length=200, mode='determinate')
vertical_progress.pack(pady=10)

Text1_label = tk.Label(right_frame, fg='white', text="Battery Level")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)
#----------------------------------------------------------------




update_progress_etlu() 
update_progress_battery()
update_time()  
start_camera_thread()

root.mainloop()
