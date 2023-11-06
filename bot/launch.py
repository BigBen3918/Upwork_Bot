from PyQt5.QtWidgets import QDialog,QApplication
from launchwindow import Ui_Form

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import threading
import time
import os
import tkinter as tk
from tkinter import messagebox

user_data_dir = r"C:/temp2"

browser = None
index = 0

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create an instance of the main window class
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.signUpButton.clicked.connect(self.signUpEvent)

        # create a separate thread to start the Chrome driver
        
    def start_new_chrome(self):
        profile_id = int(self.ui.from_id.text())
        verifyEmail = self.ui.email.text() + "+" + str(profile_id) + "@gmail.com"
        password = self.ui.password.text()
        answer = self.ui.answer.text()
        if os.path.exists(user_data_dir + "/Profile "+ str(profile_id)):
            pass
        else:
            root = tk.Tk()
            root.withdraw() # Hide the main window
            messagebox.showwarning("Warning", "There is no user whose id is " + str(profile_id))
            root.destroy()
            return            

        options.add_argument("--user-data-dir=" + user_data_dir )
        options.add_argument("--profile-directory=Profile " + str(profile_id))
        # options.add_argument("--profile-directory=Profile "+profileId)
        
        # Create a new instance of the Chrome browser with the specified options
        global browser
        browser = webdriver.Chrome(options=options)
        
        browser.get("https://www.upwork.com/login")
        time.sleep(2)
        
        if not "login" in browser.current_url:
            # browser.get("https://www.upwork.com/nx/create-profile/welcome/")
            browser.get("https://www.upwork.com/nx/jobs/search/?sort=recency&category2_uid=531770282580668418&t=0,1&amount=500-999,1000-4999,5000-&hourly_rate=25-")
        else:
            while True:
                try:
                    browser.find_element(By.ID,'login_username').send_keys(verifyEmail)
                    break
                except:
                    time.sleep(3)
                    browser.get("https://www.upwork.com/login")
                    pass
            time.sleep(0.1)
            browser.find_element(By.ID,'login_password_continue').click()
            time.sleep(2)
            browser.find_element(By.ID,'login_password').send_keys(password)
            browser.find_element(By.ID,'login_control_continue').click()
            
            time.sleep(4)

            if "login" in browser.current_url:
                try: 
                    browser.find_element(By.ID,'login_answer').send_keys(answer)
                    browser.find_element(By.ID,'login_control_continue').click()
                    time.sleep(4)
                except:
                    # browser.find_element(By.ID,'login_answer').send_keys(answer)
                    browser.find_element(By.ID,'control_cancel').click()
                    time.sleep(4)
                    


           
            browser.execute_script('''window.open("https://www.upwork.com/ab/proposals/");''')
            

            browser.execute_script('''window.open("https://www.upwork.com/ab/messages/rooms/","_blank");''')

            browser.execute_script('''window.open("https://www.upwork.com/nx/jobs/search/?sort=recency&category2_uid=531770282580668418&t=0,1&amount=500-999,1000-4999,5000-&hourly_rate=25-","_blank");''')


    def signUpEvent(self):
        global browser
        browser = None
        t = threading.Thread(target=self.start_new_chrome, args=())
        t.start()
        
    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()

    # show the main window
    window.show()

    # run the event loop
    app.exec_()

    pass