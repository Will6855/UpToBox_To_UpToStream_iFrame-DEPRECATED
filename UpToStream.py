import os
from time import sleep

# Chrome Browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# GUI
from tkinter import *

# Chrome Browser's options
s=Service(ChromeDriverManager().install())

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #Get rid of "Chrome is being controlled by automated test software"
chrome_options.add_experimental_option("detach", True) #Let browser open until manually closed


uBlock = str.replace(os.path.realpath(__file__), 'UpToStream.py', '1.44.0_1.crx')
VeePN = str.replace(os.path.realpath(__file__), 'UpToStream.py', '2.5.1_0.crx')
chrome_options.add_extension(uBlock) #Add Ublock Origin
chrome_options.add_extension(VeePN) #Add VeePN

delay = 5 #seconds

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()

sleep(3)
driver.switch_to.window(driver.window_handles[1]) #Go to VeePN Pop-Up

driver.get('chrome-extension://majdfhpaihoncoakbjgbdhglocklcgno/html/foreground.html')
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
element = driver.find_element(By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button')
element.click()

try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
element = driver.find_element(By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button')
element.click()

try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainBtn"]/span')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
element = driver.find_element(By.XPATH, '//*[@id="mainBtn"]/span')
element.click()

driver.close()
driver.switch_to.window(driver.window_handles[0]) #Go back to original tab

# Display GUI
app = Tk()
app.title("UpToBox To UpToStream")

def replace():
    url = url1.get()
    url = str.replace(url, 'uptobox.com', 'uptostream.com/iframe')
    app.quit()
    driver.get(url)

url1 = Entry(app, text='Enter UpToBox URL:')
url1.pack()

button = Button(app, text = 'Watch!', command = replace)
button.pack()

app.mainloop()
