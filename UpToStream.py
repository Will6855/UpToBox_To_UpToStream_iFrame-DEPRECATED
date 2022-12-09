import os
import sys

# Chrome Browser
from selenium import webdriver as WD
from selenium.webdriver.chrome.service import Service as S
from webdriver_manager.chrome import ChromeDriverManager as CDM
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE

# Module to remove command prompt
from subprocess import CREATE_NO_WINDOW

# App Path
app_path = str.replace(os.path.realpath(__file__), 'UpToStream.py', '')

# Chrome Browser's options
s=S(CDM().install())
o = WD.ChromeOptions()
s.creationflags = CREATE_NO_WINDOW # Remove command prompt
o.add_argument('start-maximized')
o.add_argument('--host-resolver-rules=MAP campongprecant.com 127.0.0.1')
o.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False}) # Disable "Save Password" Pop-Up
o.add_experimental_option("excludeSwitches", ['enable-automation']) # Get rid of "Chrome is being controlled by automated test software"
o.add_experimental_option("detach", True) # Let browser open until manually closed
o.add_extension(app_path + '2.5.1_0.crx') # Add VeePN

# Set delay
t = 300

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
            TE()
        d.find_element(By.XPATH, '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button').click()
    WDW(d, t).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainBtn"]/span')))
    d.find_element(By.XPATH, '//*[@id="mainBtn"]/span').click()

    # Go to link    
    d.get('https://uptobox.live')

    # Remove Ads & Replace All Uptobox Links
    while True:

        # Disable right click
        element = d.find_element(By.XPATH, "/html")
        d.execute_script("arguments[0].setAttribute('oncontextmenu', 'return false;')", element)

        # Remove Ads
        if d.title == 'Uptostream':
            # Change Window Title
            element = d.find_element(By.XPATH, '/html/body/div[1]')
            name = (str(element.get_attribute("data-ui")).split('name":"'))[1].split('"')[0]
            d.execute_script(f"document.title = '{name}'")
        if d.title != 'Uptostream':
            try:
                element = d.find_element(By.XPATH, '//*[@id="player_ima-ad-container"]')
                d.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
                # Working
            except:
                TE()

        # Replace All Uptobox Links
        if d.current_url == 'https://uptobox.live/':
            try:
                i = 0
                for elem in d.find_elements(By.XPATH, "//small/a[@href]"): # Element in Elements
                    i = i + 1
                    title = d.find_element(By.XPATH, '//*[@id="search-result"]/tbody/tr['+ str(i) +']/td[1]/div').get_attribute("title")
                    
                    # Check if file is playable
                    if title.endswith('mkv') or title.endswith('mp4') or title.endswith('avi'):
                        new_url = str(elem.get_attribute("href")).replace('uptobox.com', 'uptostream.com/iframe')
                        d.execute_script(f"arguments[0].href = '{new_url}'", elem)
                        d.execute_script(f"arguments[0].innerText = '{new_url}'", elem)
                        d.execute_script(f"arguments[0].target = ''", elem)
                    else:
                        element = d.find_element(By.XPATH, '//*[@id="search-result"]/tbody/tr['+ str(i) +']')
                        d.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
            except:
                TE()
            
except:
    d.quit()
    sys.exit()