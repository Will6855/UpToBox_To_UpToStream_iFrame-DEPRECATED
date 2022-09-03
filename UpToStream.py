import os
import sys

# Chrome Browser
from selenium import webdriver as WD
from selenium.webdriver.chrome.service import Service as S
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Module to remove command prompt
from subprocess import CREATE_NO_WINDOW

# Chrome Browser's options
s=S(str.replace(os.path.realpath(__file__), 'UpToStream.py', 'chromedriver.exe'))
o = WD.ChromeOptions()
s.creationflags = CREATE_NO_WINDOW # Remove command prompt
o.add_argument('start-maximized')
o.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False}) # Disable "Save Password" Pop-Up
o.add_experimental_option("excludeSwitches", ['enable-automation']) #Get rid of "Chrome is being controlled by automated test software"
o.add_experimental_option("detach", True) #Let browser open until manually closed
o.add_extension(str.replace(os.path.realpath(__file__), 'UpToStream.py', '1.44.0_1.crx')) #Add Ublock Origin
o.add_extension(str.replace(os.path.realpath(__file__), 'UpToStream.py', '2.5.1_0.crx')) #Add VeePN

# Set delay
t = 10

# Launch Chrome
d = WD.Chrome(service=s, options=o)
try:
    # Account connection to UpToBox.com
    d.get('https://uptobox.com/login')
    WDW(d, t).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/input[1]')))
    d.find_element(By.XPATH, '//*[@id="login-form"]/input[1]').send_keys('UpToStream_Free') # Username
    d.find_element(By.XPATH, '//*[@id="login-form"]/input[2]').send_keys('UpToStream_Free!') # Password
    d.find_element(By.XPATH, '//*[@id="login-form"]/div/button').click() # Connection

    # Go to VeePN extension and connection
    d.get('chrome-extension://majdfhpaihoncoakbjgbdhglocklcgno/html/foreground.html')
    for _ in range(2):
        try:
            WDW(d, t).until(EC.presence_of_element_located((By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button')))
        except:
            TimeoutException()
        d.find_element(By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button').click()
    WDW(d, t).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainBtn"]/span')))
    d.find_element(By.XPATH, '//*[@id="mainBtn"]/span').click()

    # Go to Uptobox.live
    d.get('https://uptobox.live')
    try:
        WDW(d, t).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-result"]/tbody/tr/td[1]/small/a')))
    except:
        TimeoutException()

    # Transform all links
    while True:
        try:
            for elem in d.find_elements(By.XPATH, "//small/a[@href]"): # Element in Elements
                new_url = str(elem.get_attribute("href")).replace('uptobox.com', 'uptostream.com/iframe')
                d.execute_script(f"arguments[0].href = '{new_url}'", elem)
                d.execute_script(f"arguments[0].innerText = '{new_url}'", elem)
        except:
            WDW(d, t).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-result"]/tbody')))

except:
    d.quit()
    sys.exit()