

import tkinter as tk
from tkinter import messagebox
import keyboard

import time
import shutil
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


with open("data.json", "r") as file:
    json_data = file.read()
data = json.loads(json_data)

with open("const.json", "r") as file:
    const_data = file.read()
const_data = json.loads(const_data)

user_data_dir = r"C:/temp2"


from_id = data["from"]
count = data["count"]
us_only = data["us_only"]

profile_id = from_id
Emial = ""


FirstName=data["FirstName"]
LastName=data["LastName"]
Password=data["Password"]
Country=data["Country"]
resume_path = data["resume_path"]
image_path = data["image_default"]
role = data["role"]
skills = data["skills"]
summary = data["summary"]
hourly = data["hourly"]
street_address = data["street_address"]
city = data["city"]
zip_code = data["zip_code"]
phone = data["phone"]

us_address = data["us_address"]
us_city = data["us_city"]
us_state = data["us_state"]
us_zip = data["us_zip"]
us_phone = data["us_phone"]

security_question = data["security_question"]

tooshort = 0.2
short = 0.5
base = 1
medium = 2.5
long = 5
toolong = 7

chrome_driver = None

def on_key_press(event):
    if event.name == 'S' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        print("s")
        signIn()
        root = tk.Tk()
        root.withdraw() # Hide the main window
        messagebox.showinfo("SingIn", "SignIn Finished")
        root.destroy()
    elif event.name == 'V' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        print("VERIFY_START")
        verify_next()
        root = tk.Tk()
        root.withdraw() # Hide the main window
        messagebox.showinfo("Verify", "Everything Finished")
        root.destroy()
    elif event.name == 'q' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        # Quit the program if ctrl+q is pressed
        print("MEIDUM")
        exit()

def signIn():
    start_chrome()
    pass

def verify_next():
    global profile_id
    profile_id = from_id
    start_verify_chrome()
    pass

def start_chrome():
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    if profile_id >= from_id + count :
        return
    options = Options()

    new_profile_dir = user_data_dir + "/" + str(profile_id)
    shutil.copytree(user_data_dir + "/Default", new_profile_dir)
    print(profile_id)
    # options.add_argument(server)

    options.add_argument("--user-data-dir=" + user_data_dir)
    options.add_argument("--profile-directory=" + str(profile_id))

    global chrome_driver
    chrome_driver = webdriver.Chrome(options=options) 

    time.sleep(short)
    signUpEvent()

def signUpEvent():
    global image_path
    if data["random"]:
        random_number = random.randint(0, 20)
        FirstName = const_data["firstName"][random_number]
        random_number = random.randint(0, 20)
        LastName = const_data["lastName"][random_number]
        random_number = random.randint(1, 10)
        image_path = data["image_path"] + str(random_number) + ".png"
    else:
        FirstName = data['FirstName']
        LastName = data['LastName']

    global profile_id
    while True:
        try:
            time.sleep(medium)   
            chrome_driver.set_window_size(600, 1000)
            break
        except:
            pass
    time.sleep(base * 1.5)

        
    while True:
        try:
            page_url = 'https://www.upwork.com/nx/signup/'
            chrome_driver.get(page_url)
            time.sleep(medium)   
            accept = chrome_driver.find_element(By.ID, "onetrust-accept-btn-handler")
            break
        except:
            pass

    
    chrome_driver.execute_script("arguments[0].click();", accept)
    time.sleep(base)

    work = chrome_driver.find_element(By.XPATH, "//*[@data-qa='work']")
    work.click()

    apply = chrome_driver.find_element(By.XPATH, '//*[@data-qa="btn-apply"]')
    apply.click()

    chrome_driver.find_element(By.ID,'first-name-input').send_keys(FirstName)
    chrome_driver.find_element(By.ID,'last-name-input').send_keys(LastName)
    Email=data["Email"] + "+" + str(profile_id) + "@gmail.com"
    chrome_driver.find_element(By.ID,'redesigned-input-email').send_keys(Email)

    chrome_driver.find_element(By.ID,'password-input').send_keys(Password)
    
    select_country = chrome_driver.find_element(By.XPATH, "//div[@class='up-dropdown-toggle-title']")
    chrome_driver.execute_script("arguments[0].click();", select_country)
    while True:
        try:

            time.sleep(medium)
            chrome_driver.find_element(By.XPATH, "//input[@autocomplete='country-name']").send_keys(Country)
            break
        except:
            pass
    
    time.sleep(short)
    item = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
    chrome_driver.execute_script("arguments[0].click();", item)
    time.sleep(short)
    
    terms = chrome_driver.find_element(By.ID, "checkbox-terms")
    chrome_driver.execute_script("arguments[0].click();", terms)
    
    time.sleep(tooshort)
    sign = chrome_driver.find_element(By.ID, "button-submit-form")
    chrome_driver.execute_script("arguments[0].click();", sign)
    time.sleep(medium)
    chrome_driver.close()

    shutil.copytree(user_data_dir + "/"+str(profile_id), user_data_dir + "/Profile "+str(profile_id))
    profile_id=profile_id+1  
    
    start_chrome()

def start_verify_chrome():      
    global chrome_driver  
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    if profile_id>= from_id + count:
        return
    
    options = Options()
    # options.add_argument(server)

    options.add_argument("--user-data-dir=" + user_data_dir)
    options.add_argument("--profile-directory=" + str(profile_id))
    chrome_driver = webdriver.Chrome(options=options) 

    time.sleep(base)
    verify()
    next()
    
def verify():
    verifyEmail=data["Email"] + "+" + str(profile_id) + "@gmail.com"
    with open("email-verify.json", "r") as file:
        email_data = file.read()
    email_data = json.loads(email_data)
    page_url = email_data[verifyEmail]
    
    chrome_driver.get(page_url)
    while True:
        try:
            
            chrome_driver.find_element(By.ID,'login_username').send_keys(verifyEmail)
            break
        except:
            time.sleep(long)
            chrome_driver.get(page_url)
            pass
    time.sleep(0.1)
    chrome_driver.find_element(By.ID,'login_password_continue').click()
    time.sleep(medium)
    chrome_driver.find_element(By.ID,'login_password').send_keys(Password)

    chrome_driver.find_element(By.ID,'login_control_continue').click()
    time.sleep(medium)

def next():
    first()
    upload()
    certification()
    skills_f()
    horuly()
    pofile()
    submit()

    if us_only:
        tax()
        contactinfo()
    chrome_driver.close()

    global profile_id
    print("profile_id, " + str(profile_id))
    profile_id=profile_id + 1
    start_verify_chrome()
    # chrome_driver.quit()

def first():
    window_size = chrome_driver.get_window_size()
    height = window_size['height']
    chrome_driver.set_window_size(1200, height)
    time.sleep(base)

    page_url = 'https://www.upwork.com/nx/create-profile/welcome/'
    chrome_driver.get(page_url)
    time.sleep(medium)
    verifyEmail=data["Email"] + "+" + str(profile_id) + "@gmail.com"
    with open("email-verify.json", "r") as file:
        email_data = file.read()
    email_data = json.loads(email_data)
    page_url = email_data[verifyEmail]
    while True:
        try:
            if not "login" in chrome_driver.current_url:
                break
            else:
                verify()
        except:
            pass
    while True:
        try:
            if not "please-verify" in chrome_driver.current_url:
                break
            else:
                chrome_driver.get(page_url)
        except:
            pass
    count =6
    while count>0:
        try:
            cross=chrome_driver.find_element(By.XPATH,'//*[@class="onetrust-close-btn-handler banner-close-button ot-close-icon"]')
            cross.click()
            break
        except:
            count = count - 1
            time.sleep(base * 1.5)
            pass
    while True:
        try:
            time.sleep(short)
            getstart = chrome_driver.find_element(By.XPATH,'//*[@class="air3-btn air3-btn-primary mr-7"]')
            
            getstart.click()
            break
        except:
            time.sleep(base)
            pass
    time.sleep(medium)
    page_url = 'https://www.upwork.com/nx/create-profile/experience/'
    chrome_driver.get(page_url)
    time.sleep(medium)
    # step2
    chrome_driver.find_element(By.XPATH, '//input[@value="FREELANCED_BEFORE"]').click()
    
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(short)

    # step3
    page_url = 'https://www.upwork.com/nx/create-profile/goal/'
    chrome_driver.get(page_url)
    time.sleep(medium)
    chrome_driver.find_element(By.XPATH, '//input[@value="MAIN_INCOME"]').click()
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(medium)

    #step4
    # page_url = 'https://www.upwork.com/nx/create-profile/welcome/'
    # chrome_driver.get(page_url)
    while True:
        try:
            time.sleep(base)
            panel = chrome_driver.find_element(By.XPATH, '//input[@data-ev-label="button_box_checkbox"]')
            chrome_driver.execute_script("arguments[0].click();", panel)
            time.sleep(base)
            step4checkbox = chrome_driver.find_element(By.XPATH, '//input[@class="air3-checkbox-input sr-only"]')
            chrome_driver.execute_script("arguments[0].click();", step4checkbox)
            time.sleep(short)
            chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
            break
        except:
            time.sleep(base)
            pass
    
    time.sleep(long)
    
def upload():
    print("upload before")
    page_url = 'https://www.upwork.com/nx/create-profile/resume-import/'
    chrome_driver.get(page_url)
    time.sleep(medium)
    print("uploading")

    while True:
        try:
            time.sleep(base)

            chrome_driver.find_element(By.XPATH, "//div[@class='d-flex flex-column']/button[2]").click()
            break
        except:
            pass
        
        
    time.sleep(short)
    
    file_input = chrome_driver.find_element(By.XPATH, "//input[@type='file']")
    
    # file_input.send_keys(os.path.dirname(os.path.abspath(__file__))+"/"+resume_path)
    file_input.send_keys(resume_path)

    time.sleep(toolong)
    while True:
        try:
            time.sleep(base)

            continuebtn = chrome_driver.find_element(By.XPATH, "//button[@class='air3-btn air3-btn-primary mb-0']")
            chrome_driver.execute_script("arguments[0].click();", continuebtn)
            break
        except:
            pass
    
    time.sleep(base)

    # step 6
    input_role = chrome_driver.find_element(By.XPATH, "//input[@type='text']")
    input_role.clear()
    input_role.send_keys(role)

    # time.sleep(0.1)
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base * 1.5) 

    # step 7
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base * 1.5) 

    # step 8
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base * 1.5) 
    
    # pass
def certification():
    print("cert")

    # page_url = 'https://www.upwork.com/nx/create-profile/certifications/'
    # chrome_driver.get(page_url)
    # time.sleep(5)

    # step 9
    current_url = chrome_driver.current_url
    if "certifications" in current_url:
        # step9checkbox = chrome_driver.find_element(By.XPATH, '//input[@class="air3-checkbox-input sr-only"]')

        # chrome_driver.execute_script("arguments[0].click();", step9checkbox)

        chrome_driver.find_element(By.XPATH, '//*[@data-test="skip-button"]').click()
        time.sleep(short)
    else:

        chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base)   
    # step 10
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(medium) 

def skills_f():
    # skills
    # page_url = 'https://www.upwork.com/nx/create-profile/skills/'
    # chrome_driver.get(page_url)    
    
    time.sleep(medium)
    
    for skill in skills:
        while True:
            try:
                input_list = chrome_driver.find_element(By.XPATH, "//input[@type='search']")
                break
            except:
                time.sleep(base)
                pass
            
        input_list.send_keys(skill)
        time.sleep(short)
        while True:
            try:
                time.sleep(base)

                item = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
                break
            except:
                a = chrome_driver.find_element(By.XPATH, "//input[@type='search']")
                a.send_keys(skill)
                time.sleep(short)

                pass
        
        chrome_driver.execute_script("arguments[0].click();", item)
    
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base) 

    # step12
    while True:
        try:
            time.sleep(base)
            input_summary = chrome_driver.find_element(By.XPATH, "//textarea[@class='air3-textarea form-control']")
            input_summary.clear()
            input_summary.send_keys(summary)
            break
        except:
            pass
    

    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base * 2) 

    # step13
    while True:
        try:
            time.sleep(base)
            chrome_driver.find_element(By.XPATH, "//button[@aria-label='Web Development']").click()
            # chrome_driver.find_element(By.XPATH, "//button[@aria-label='Ecommerce Development']").click()
            # chrome_driver.find_element(By.XPATH, "//button[@aria-label='AI & Machine Learning']").click()
            # chrome_driver.find_element(By.XPATH, "//button[@aria-label='Mobile Development']").click()
            break
        except:
            pass
    
    while True:
        try:
            time.sleep(base)
            chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
            break
        except:
            pass
    
    time.sleep(1.5) 

def horuly():
    # page_url = 'https://www.upwork.com/nx/create-profile/rate/'
    # chrome_driver.get(page_url)    
    time.sleep(medium) 
    # step14
    
    input_hourly = chrome_driver.find_element(By.XPATH, '//input[@data-test="currency-input"]')
    input_hourly.clear()
    input_hourly.send_keys(hourly)
    time.sleep(tooshort) 
    chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    time.sleep(base) 

def pofile():
    # page_url = 'https://www.upwork.com/nx/create-profile/location/'
    # chrome_driver.get(page_url)    
    time.sleep(base) 
    # step15
    upload = chrome_driver.find_element(By.XPATH, "//button[@data-qa='open-loader']")
    chrome_driver.execute_script("arguments[0].click();", upload)
    time.sleep(medium)
    while True:
        try:

            file_input = chrome_driver.find_element(By.NAME, "imageUpload")
            break
        except:
            time.sleep(base)
            
    # file_input.send_keys(os.path.dirname(os.path.abspath(__file__))+"/"+image_path)
    file_input.send_keys(image_path)
    time.sleep(medium)
    attach = chrome_driver.find_element(By.XPATH, "//button[contains(text(), 'Attach photo')]")
    chrome_driver.execute_script("arguments[0].click();", attach)
    time.sleep(toolong)
    while True:
        try:
            chrome_driver.find_element(By.XPATH, "//input[@aria-labelledby='street-label']").clear()
            
            chrome_driver.find_element(By.XPATH, "//input[@aria-labelledby='street-label']").send_keys(street_address)
            chrome_driver.find_element(By.XPATH, "//input[@aria-labelledby='postal-code-label']").clear()
            chrome_driver.find_element(By.XPATH, "//input[@aria-labelledby='postal-code-label']").send_keys(zip_code)
            chrome_driver.find_element(By.XPATH, "//input[@inputmode='numeric']").clear()
            chrome_driver.find_element(By.XPATH, "//input[@inputmode='numeric']").send_keys(phone)

            chrome_driver.find_element(By.XPATH, "//input[@aria-labelledby='city-label']").send_keys(city)
            time.sleep(medium)
            item_city = chrome_driver.find_element(By.XPATH, "//span[@class='air3-menu-item-text']")
            chrome_driver.execute_script("arguments[0].click();", item_city)
            time.sleep(short)
            chrome_driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
            break
        except:
            time.sleep(base)
            pass
        
    # submit()

def submit():
    page_url = 'https://www.upwork.com/nx/create-profile/submit/'
    chrome_driver.get(page_url)    
    time.sleep(medium)

    # submit
    while True:
        try:
            time.sleep(base)
            submit = chrome_driver.find_element(By.XPATH, '//button[@class="air3-btn air3-btn-primary width-md m-0"]')
            break
        except:
            pass
    
    
    chrome_driver.execute_script("arguments[0].click();", submit)

    # browser
    # page_url = 'https://www.upwork.com/nx/create-profile/finish/'
    # chrome_driver.get(page_url)    
    # time.sleep(medium)
    while True:
        try:
            time.sleep(base)
            browser = chrome_driver.find_element(By.XPATH, "//a[@class='up-n-link air3-btn air3-btn-primary']")
            break
        except:
            pass
    
    chrome_driver.execute_script("arguments[0].click();", browser)
    time.sleep(medium)

def tax():
    window_size = chrome_driver.get_window_size()
    height = window_size['height']

    chrome_driver.set_window_size(600, height)
    time.sleep(base)

    page_url = 'https://www.upwork.com/nx/tax/'
    chrome_driver.get(page_url)    
    # chrome_driver.get(page_url)    
    time.sleep(long)

    current_url = chrome_driver.current_url

    bPassword = True
    # check password and security
    if "reenter-password" in current_url:

        time.sleep(short)
        chrome_driver.find_element(By.ID, 'sensitiveZone_password').send_keys(Password)
        time.sleep(short)
        chrome_driver.find_element(By.ID, 'control_save').click()
        bPassword = False
        time.sleep(medium)

    # time.sleep(3)
    if "security-question" in current_url:
        print("security-quettion page")
        time.sleep(1)
        while True:
            try:
                chrome_driver.find_element(By.ID, 'securityQuestion_answer').clear()
                chrome_driver.find_element(By.ID, 'securityQuestion_answer').send_keys(security_question)

                seccombo1 = chrome_driver.find_element(By.ID, "lockingNotice")
                chrome_driver.execute_script("arguments[0].click();", seccombo1)
                time.sleep(base)

                seccombo2 = chrome_driver.find_element(By.ID, "remember")
                chrome_driver.execute_script("arguments[0].click();", seccombo2)

                chrome_driver.find_element(By.ID, 'control_save').click()
                time.sleep(medium)
                break
            except:
                pass
        
    else:
        print("No security-question page")

        if "reenter-password" in current_url and bPassword:
            print("reenter-password")
            time.sleep(short)
            chrome_driver.find_element(By.ID, 'sensitiveZone_password').send_keys(Password)
            time.sleep(short)
            chrome_driver.find_element(By.ID, 'control_save').click()
            time.sleep(medium)
        else:
            print("No password page")
    
    # TAX
    print("TAX")
    
    time.sleep(short)
    while True:
        try:
            plus_btm = chrome_driver.find_element(By.XPATH, "//button[@data-qa='tax-residency-form-header-button']")
            chrome_driver.execute_script("arguments[0].click();", plus_btm)
            break
        except:
            time.sleep(short)
            pass
    
    # country-united
    while True:
        try:

            select_country = chrome_driver.find_element(By.XPATH, "//div[@class='air3-dropdown-toggle']")
            chrome_driver.execute_script("arguments[0].click();", select_country)
            
            break
        except:
            time.sleep(short)
            pass
    while True:
        try:
            time.sleep(medium)
            chrome_driver.find_element(By.XPATH, "//input[@aria-autocomplete='list']").send_keys("United States")
            break
        except:
            time.sleep(base)
            pass
    
    time.sleep(base)
    
    while True:
        try:
            item_country = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
            chrome_driver.execute_script("arguments[0].click();", item_country)
    
            break
        except:
            time.sleep(short)
            pass
    time.sleep(medium)
    # end
    while True:
        try:
            chrome_driver.find_element(By.ID, 'address-street').send_keys(us_address)
            chrome_driver.find_element(By.ID, 'address-city').send_keys(us_city)
            chrome_driver.find_element(By.ID, 'address-zip').send_keys(us_zip)
    
            break
        except:
            time.sleep(short)
            pass
    
    # state-U.S
    while True:
        try:
            select_countries = chrome_driver.find_elements(By.XPATH, "//div[@class='air3-dropdown-toggle']")
    
            break
        except:
            time.sleep(short)
            pass
    time.sleep(tooshort)
    while True:
        try:
            select_country = select_countries[1]
            chrome_driver.execute_script("arguments[0].click();", select_country)
    
            break
        except:
            time.sleep(base)
            pass

    while True:
        try:
            chrome_driver.find_element(By.XPATH, "//input[@enterkeyhint='search']").send_keys(us_state)

            break
        except:
            time.sleep(short)
            pass
    time.sleep(short)
    while True:
        try:
            item_state = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
            chrome_driver.execute_script("arguments[0].click();", item_state)
    
            break
        except:
            time.sleep(short)
            pass
    time.sleep(short)
    # end
    while True:
        try:
            
            save_btn = chrome_driver.find_element(By.XPATH, "//button[@data-qa='tax-residency-form-submit-button']")
            chrome_driver.execute_script("arguments[0].click();", save_btn)

            break
        except:
            time.sleep(short)
            pass
    
    time.sleep(base)
    while True:
        try:

            confirm_address = chrome_driver.find_element(By.XPATH, "//button[@class='air3-btn air3-btn-primary air3-btn-block-sm']")
            chrome_driver.execute_script("arguments[0].click();", confirm_address)
    
            break
        except:
            time.sleep(base)
            pass

    time.sleep(medium)
    # next
    while True:
        try:

            edit_next = chrome_driver.find_element(By.XPATH, "//button[@data-qa='tax-info-form-header-button']")
            chrome_driver.execute_script("arguments[0].click();", edit_next)
        
            break
        except:
            time.sleep(base)
            pass
    

    while True:
        try:
            print("4")

            us_types = chrome_driver.find_elements(By.XPATH, "//input[@name='type']")
            us_type = us_types[1]
            chrome_driver.execute_script("arguments[0].click();", us_type)

            tax_name = FirstName + " " + LastName
            chrome_driver.find_element(By.ID, "legalName").send_keys(tax_name)
            break
        except:
            time.sleep(short)
            pass
    

    # select tax
    while True:
        try:
            print("5")

            select_tax = chrome_driver.find_element(By.XPATH, "//div[@class='air3-dropdown-toggle-title']")
            chrome_driver.execute_script("arguments[0].click();", select_tax)
            break
        except:
            time.sleep(short)
            pass
    
    while True:
        try:
            print("6")

            item_tax = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
            chrome_driver.execute_script("arguments[0].click();", item_tax)
    
            break
        except:
            time.sleep(medium)
            pass
    # end
    while True:
        try:
            print("7")

            ssnType = chrome_driver.find_element(By.XPATH, "//input[@name='ssnType']")
            chrome_driver.execute_script("arguments[0].click();", ssnType)
    
            break
        except:
            time.sleep(base)
            pass
        
    while True:
        try:
            chrome_driver.find_element(By.ID, "tin").send_keys("875-96-5698")

            chrome_driver.find_element(By.ID, "signature-input").send_keys(tax_name)

            scroll_down = chrome_driver.find_element(By.XPATH, "//div[@class='certification-context']")
            chrome_driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_down)

            item_checkboxs = chrome_driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            item_checkbox0 = item_checkboxs[0]
            item_checkbox1 = item_checkboxs[1]
            chrome_driver.execute_script("arguments[0].click();", item_checkbox0)
            chrome_driver.execute_script("arguments[0].click();", item_checkbox1)
            break
        except:
            time.sleep(base)
            pass

    while True:
        try:
            btn_save = chrome_driver.find_element(By.XPATH, "//button[@class='air3-btn air3-btn-primary mb-0']")
            chrome_driver.execute_script("arguments[0].click();", btn_save)
    
            break
        except:
            time.sleep(base)
            pass
    pass

def contactinfo():
    page_url = 'https://www.upwork.com/freelancers/settings/contactInfo'
    chrome_driver.get(page_url)    
    time.sleep(medium)

    current_url = chrome_driver.current_url

    bPassword = True
    # check password and security
    if "reenter-password" in current_url:
        print("reenter-password")
        time.sleep(medium)
        while True:
            try:
                chrome_driver.find_element(By.ID, 'sensitiveZone_password').send_keys(Password)
            
                break
            except:
                time.sleep(base)
                pass
        bPassword = False
        time.sleep(base)
        contactinfo()
        return
    else:
        print("No password page")

    # time.sleep(3)
    if "security-question" in current_url:
        print("security-quettion page")
        time.sleep(base)
        while True:
            try:
                chrome_driver.find_element(By.ID, 'securityQuestion_answer').send_keys(security_question)

                break
            except:
                time.sleep(base)
                pass
        while True:
            try:
                seccombobase = chrome_driver.find_element(By.ID, "securityQuestion_lockingNotice")
                chrome_driver.execute_script("arguments[0].click();", seccombobase)
                break
            except:
                time.sleep(base)
                pass
        
        while True:
            try:
                seccombo2 = chrome_driver.find_element(By.ID, "securityQuestion_remember")
                chrome_driver.execute_script("arguments[0].click();", seccombo2)

                chrome_driver.find_element(By.ID, 'control_save').click()
                break
            except:
                time.sleep(short)
                pass
        
        time.sleep(medium)
        contactinfo()
        return
    else:
        print("No security-question page")

        if "reenter-password" in current_url and bPassword:
            print("reenter-password")
            while True:
                try:
                    chrome_driver.find_element(By.ID, 'sensitiveZone_password').send_keys(Password)
                    break
                except:
                    time.sleep(short)
                    pass
            
            while True:
                try:
                    chrome_driver.find_element(By.ID, 'control_continue').click()

                    break
                except:
                    time.sleep(short)
                    pass
            time.sleep(medium)
        else:
            print("No password page")
    time.sleep(base)
    chrome_driver.execute_script("window.scrollTo(0, Math.ceil(document.documentElement.scrollHeight / 4))")

    while True:
        try:
            edit_location = chrome_driver.find_element(By.XPATH, "//button[@aria-label='Edit location']")
            chrome_driver.execute_script("arguments[0].click();", edit_location)
    
            break
        except:
            time.sleep(base)
            pass
    time.sleep(2)
    while True:
        try:
            select_countries = chrome_driver.find_elements(By.XPATH, "//div[@class='up-dropdown-toggle-title']")
            select_country = select_countries[1]
            chrome_driver.execute_script("arguments[0].click();", select_country)
    
            break
        except:
            time.sleep(short)
            pass
    # country-united
    time.sleep(1.5)
    while True:
        try:
            chrome_driver.find_element(By.XPATH, "//input[@class='up-input']").send_keys("United States")
    
            break
        except:
            time.sleep(short)
            pass
    
    time.sleep(short)
    while True:
        try:
            item_country = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
            chrome_driver.execute_script("arguments[0].click();", item_country)
    
            break
        except:
            time.sleep(short)
            pass
    time.sleep(short)
    # end
    while True:
        try:
            fake = chrome_driver.find_element(By.XPATH, "//input[@class='up-typeahead-input-fake up-input']")
            chrome_driver.execute_script("arguments[0].focus();", fake)
    
            break
        except:
            time.sleep(short)
            pass
    
    time.sleep(base)
    while True:
        try:
            full_address = us_address + ", " + us_city
            chrome_driver.find_element(By.XPATH, "//input[@class='up-typeahead-input-main up-input']").send_keys(full_address)
    
            break
        except:
            time.sleep(short)
            pass
    time.sleep(short)
    while True:
        try:
            item_address = chrome_driver.find_element(By.XPATH, "//li[@role='option']")
            chrome_driver.execute_script("arguments[0].click();", item_address)
    
            break
        except:
            time.sleep(short)
            pass
    time.sleep(base)
    while True:
        try:
            phone_number = chrome_driver.find_element(By.XPATH, "//input[@type='tel']")
            phone_number.clear()
            phone_number.send_keys(us_phone)
            break
        except:
            time.sleep(short)
            pass
    
    time.sleep(short)
    while True:
        try:
            save = chrome_driver.find_element(By.XPATH, "//button[@data-test='updateLocation']")
            chrome_driver.execute_script("arguments[0].click();", save)

            save = chrome_driver.find_element(By.XPATH, "//button[@class='up-btn up-btn-sm up-btn-primary']")
            chrome_driver.execute_script("arguments[0].click();", save)
            break
        except:
            time.sleep(short)
            pass
    
    pass

keyboard.on_press(on_key_press)
keyboard.wait()

