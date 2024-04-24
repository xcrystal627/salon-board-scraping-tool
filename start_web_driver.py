import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
from datetime import  datetime 
from retrying import retry
from bs4 import BeautifulSoup
import threading
import time
import urllib
import json
import re



def start_driver():

    try:
        options = Options()     
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--disable-features=NetworkService')
        options.add_argument('--enable-features=NetworkServiceInProcess')
        options.add_argument('--disable-domain-reliability')
        options.add_argument('--log-level=0')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)


        # install stable latest version chrome driver  
        try: 
            driver = webdriver.Chrome( service=Service(ChromeDriverManager().install()), options=options )  
        except ValueError:            
            latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
            service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
            
            driver = webdriver.Chrome(service=service, options=options)

        except Exception as error:
            print(error)
            return None
        
        return driver

    except Exception as error:
        print(error)
        driver.quit()
        return None
    