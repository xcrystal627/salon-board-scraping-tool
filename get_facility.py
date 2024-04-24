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
from api.facility import update_and_register_facility_for_one_salon


SHORT_WAIT_TIME = 2
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5



def scrape_and_register_facility_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons

    
    for salon in all_salons:
        driver = start_driver()

        if driver == None:
            print('While starting driver, occur error')    
            return
            
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_facility_from_saloboard(driver, salon['id'])



def get_facility_from_saloboard(driver, salon_id):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/CNK/set/equipList/')

    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "equipListhForm"))
        )   
    except TimeoutError as e:
        driver.quit()
        return

    facility_tables_div = driver.find_element(By.CSS_SELECTOR, 'div.tab01')
    facility_tables = facility_tables_div.find_elements(By.XPATH, '//table[(@style="display: block;") and (contains(@class, "equipment_table"))]')


    for idx in range(len(facility_tables)):
        
        if idx == 0:
            continue

        try:
            table_tr = facility_tables[idx].find_element(By.CSS_SELECTOR, 'tr.mod_middle')
            table_tr_datas = table_tr.find_elements(By.TAG_NAME, 'td')
            
            facility_name = table_tr_datas[1].find_element(By.XPATH, 'input[@type="text"]').get_attribute('value')
            selected_possible_count = table_tr_datas[2].find_element(By.XPATH, "//option[@selected='selected']").get_attribute('value')

            res_data = {
                "salon_id"      : str(salon_id),
                "name"          : facility_name,
                "count"         : selected_possible_count,
                "order"         : idx               
            }
            
            update_and_register_facility_for_one_salon(json_data=json.dumps(res_data))

        except Exception as e:
            print(e)

        time.sleep(1)
        

    driver.quit()


def scrape_facility_thread():
    while 1:
        scrape_and_register_facility_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_facility_thread)
    my_thread.start()
    my_thread.join()
