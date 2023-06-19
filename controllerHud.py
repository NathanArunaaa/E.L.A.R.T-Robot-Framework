import cv2
import customtkinter
import tkinter as tk
from PIL import ImageTk, Image
import threading

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

        # Create the video source and start the streaming thread
        self.vid = cv2.VideoCapture(0)
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            ret, frame = self.vid.read()
            if ret:
                # Resize the frame to a larger size
                desired_width = 800
                aspect_ratio = frame.shape[1] / frame.shape[0]
                desired_height = int(desired_width / aspect_ratio)
                frame = cv2.resize(frame, (desired_width, desired_height))

                # Convert the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Create an ImageTk object from the frame
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

                # Update the label with the new frame
                self.label.configure(image=photo)
                self.label.image = photo

            # Break the loop if the window is closed
            if not self.master.winfo_exists():
                self.vid.release()
                break

            # Delay for a short interval between frames
            self.master.after(1)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Adjust the window size as needed
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

app = App()
app.mainloop()
