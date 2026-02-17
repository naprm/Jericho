import os
import sys
import requests
import tkinter as tk
import time
from datetime import datetime
import threading
from tkinter import messagebox
import customtkinter as ctk
import keyring
from PIL import Image
import cv2

WAIT_TIME = 30
WELCOME_TIME = 5


import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




class Emoticons:
    exclamation = u'\U00002757'
    siren = u'\U0001F6A8'
    warning_sign = u"\U000026A0\U0000FE0F"
    clock = u"\U0001F552"



class telegram_actions():
    def __init__(self):
        self.jericho_token = keyring.get_password("Jericho", "BOT_TOKEN")
        self.chat_id = keyring.get_password("Jericho", "CHAT_ID") # os.environ.get("chat_id") #
    
    def send_message(self,msg):
        url = f"https://api.telegram.org/bot{self.jericho_token}/sendMessage"
        parameters = {
            "chat_id": self.chat_id,
            "text": msg,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, data=parameters, timeout=10)
        except Exception as error:
            print("Something Wrong Happened when trying to contact Jericho")
            print(error)
    
    def send_image(self):
        url = f"https://api.telegram.org/bot{self.jericho_token}/sendPhoto"
        frame = cam_capture()

        success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not success:
            self.send_message("Image encoding failed")
            return

        files = {
            "photo": ("capture.jpg", buffer.tobytes(), "image/jpeg")
        }

        parameters = {
            "chat_id": self.chat_id,
        }
        try:
            requests.post(url, data=parameters,files=files, timeout=10)
        except Exception as error:
            print("Something Wrong Happened when trying to contact Jericho")
            print(error)


def cam_capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    time.sleep(2)  # allow camera to warm up
    ret, frame = cap.read()
    cap.release()
    return frame


def wait_for_internet():
    # * Wait until internet is available.

    while True:
        try:
            requests.get("https://www.google.com", timeout=5)
            return
        except requests.ConnectionError:
            time.sleep(30)



class PasswordPrompt():
    def __init__(self):
        self.app = ctk.CTk()
        ctk.set_appearance_mode("system")  # or "dark"/"light"
        ctk.set_default_color_theme("blue")

        self.app.title("Authentication Required")
        self.app.geometry("720x480")
        self.app.resizable(False, False)
        self.app.eval('tk::PlaceWindow . center')

        self.password_entered = None
        self.start_time = time.time()



        # * Image label
        img = ctk.CTkImage(light_image=Image.open(resource_path('./Jericho.PNG')),
                           dark_image=Image.open(resource_path("./Jericho.PNG")),
                           size=(100, 90))
        self.app.img_label = ctk.CTkLabel(self.app, image=img, text="")  # no text
        self.app.img_label.pack(pady=(90, 5))



        # * Heading Label
        self.app.label = ctk.CTkLabel(self.app, text="Enter Password", font=("Arial", 24))
        self.app.label.pack(pady=20)



        # *Password Show and Hide Icons
        self.eye_open_img = ctk.CTkImage(
            light_image=Image.open(resource_path("./show.png")),
            dark_image=Image.open(resource_path("./show.png")),
            size=(16, 16)
        )
        self.eye_closed_img = ctk.CTkImage(
            light_image=Image.open(resource_path("./hide.png")),
            dark_image=Image.open(resource_path("./hide.png")),
            size=(16, 16)
        )



        # * Adding Grid Frame for having password box and show password icon on the same line
        self.app.input_frame = ctk.CTkFrame(self.app)
        self.app.input_frame.pack(pady=10)

        self.app.entry = ctk.CTkEntry(self.app.input_frame, show="*", font=("Arial", 16), width=250)
        self.app.entry.grid(row=0, column=0, padx=(10, 10), pady=10)
        self.app.entry.bind("<Return>", lambda event: self.submit())

        self.showing_password = False
        self.app.toggle_button = ctk.CTkButton(self.app.input_frame,text="",image=self.eye_closed_img,width=10,command=self.toggle_password,fg_color="#47A4F5")
        self.app.toggle_button.grid(row=0,column=1, padx=(0, 10))

        
        
        # * Submit Buttom 
        self.app.submit_button = ctk.CTkButton(self.app, text="Submit", font=("Arial", 16), command=self.submit)
        self.app.submit_button.pack(pady=20)
        

        
        # *Countdown label
        self.app.countdown_label = ctk.CTkLabel(self.app, text="", font=("Arial", 14))
        self.app.countdown_label.pack(pady=5)

        self.app.after(100, self.update_countdown)
        self.app.after(100, lambda: self.app.entry.focus_force())
        self.app.mainloop()
    


    # * Function to pull the Password Entered on the click of Submit button
    def submit(self):
        self.password_entered = self.app.entry.get()
        self.app.destroy()



    # * Function to show the time left to enter the password
    def update_countdown(self):
        if not self.app.winfo_exists():
            return
        remaining = int(WAIT_TIME - (time.time() - self.start_time))
        if remaining > 0:
            self.app.countdown_label.configure(text=f"Time left: {remaining}s")
            self.app.after(500, self.update_countdown)
        else:
            self.submit()
    


    # * Switch between showing and hiding password.
    def toggle_password(self):
        if self.showing_password:
            # * Hides password
            self.app.entry.configure(show="*")
            self.app.toggle_button.configure(image=self.eye_closed_img)
            self.showing_password = False
        else:
            # * Shows password
            self.app.entry.configure(show="")
            self.app.toggle_button.configure(image=self.eye_open_img)
            self.showing_password = True




def welcome_message():
        app = ctk.CTk()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        app.title("Welcome")
        app.geometry("600x300")
        app.eval('tk::PlaceWindow . center')
        app.resizable(False, False)

        app.label = ctk.CTkLabel(app, text="Welcome Back Boss !!", font=("Arial", 28, "bold"))
        app.label.pack(expand=True)

        app.after(WELCOME_TIME * 1000, app.destroy)
        app.mainloop()




def main():
    app = PasswordPrompt()
    entered_pass = app.password_entered
    passkey = keyring.get_password("LN_APP", "PASSKEY")
    if entered_pass != passkey:
        wait_for_internet()
        now = datetime.now()
        formatted_time = now.strftime("%d/%m/%Y %H:%M:%S")
        #print(formatted_time)
        message = f"{(Emoticons.siren)*3}  *SYSTEM LOGIN ALERT*  {(Emoticons.siren)*3}\n\n{Emoticons.warning_sign}  Unauthorized login detected!\n\n{Emoticons.clock} *Time:* {formatted_time}\n"
        #print(message)
        telegram = telegram_actions()
        telegram.send_message(message)
        telegram.send_image()
    else:
        welcome_message()


if __name__ == "__main__":
    main()