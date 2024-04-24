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
from api.salon import get_all_salon_information
from salonboard_login import login_salonboard
from start_web_driver import start_driver
from api.menu import update_and_register_menu_item_for_one_salon 



SHORT_WAIT_TIME = 2
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5



def scrape_and_register_menu_item_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons

    
    for salon in all_salons:
        driver = start_driver()

        if driver == None:
            print('While starting driver, occur error')    
            return
            
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_menu_item_from_saloboard(driver, salon['id'])



def get_menu_item_from_saloboard(driver, salon_id):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/CNK/set/menuSet/')

    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "menuSetForm"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    display_menu_set_tables = driver.find_elements(By.XPATH, '//table[@style="display: table;" and (contains(@class, "menuSetTable"))]')
    

    for idx in range(len(display_menu_set_tables)):
        
        try:
            table_datas = display_menu_set_tables[idx].find_elements(By.CSS_SELECTOR, 'td')
            menu_category = table_datas[1].find_element(By.CSS_SELECTOR, 'label.label_genre_ctgr_name').text
            menu_category = menu_category.replace('\n',', ')

            menu_name = table_datas[1].find_element(By.ID, 'text_menuName').get_attribute('value')

            menu_cost = table_datas[2].find_element(By.ID, 'text_price').get_attribute('value')

            menu_required_time = table_datas[3].find_element(By.CSS_SELECTOR, 'input.jscConvertTimeInput').get_attribute('value')

            res_data = {
                "salon_id"      : str(salon_id),
                "name"          : menu_name,
                "cost"          : menu_cost,
                "description"   : '',
                "required_time" : menu_required_time,
                "category"      : menu_category,
                "image"         : ''
            }

            update_and_register_menu_item_for_one_salon(json_data=json.dumps(res_data))
        
        except Exception as e:
            print(e)
        
        time.sleep(1)
        
        



    driver.quit()


def scrape_menu_item_thread():
    while 1:
        scrape_and_register_menu_item_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_menu_item_thread)
    my_thread.start()
    my_thread.join()
