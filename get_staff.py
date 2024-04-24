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



SHORT_WAIT_TIME = 2
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5



def scrape_and_register_staff_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons

    
    for salon in all_salons:
        driver = start_driver()

        if driver == None:
            print('While starting driver, occur error')    
            return
        
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_staff_from_saloboard(driver, salon['id'])



def get_staff_from_saloboard(driver, salon_id):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/CNK/set/staffSetup/')

    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "staffForm"))
        )   
    except TimeoutError as e:
        driver.quit()
        return

    staff_tables_div = driver.find_element(By.ID, 'mainDiv')
    staff_tables = staff_tables_div.find_elements(By.XPATH, '//table[(@style="display: block;") and (contains(@class, "staff_table"))]')


    for idx in range(len(staff_tables)):
        
        try:
            table_tr = staff_tables[idx].find_element(By.CSS_SELECTOR, 'tr.mod_middle')
            table_tr_datas = table_tr.find_elements(By.CSS_SELECTOR, 'td.border-right')
            
            name_elements = table_tr_datas[1].find_elements(By.XPATH, '//input[@type="text"]')
            name = name_elements[0].get_attribute('value') + '' + name_elements[1].get_attribute('value')
            name_kana = name_elements[2].get_attribute('value') + '' + name_elements[3].get_attribute('value')

            selected_gender_element = table_tr_datas[2].find_element(By.XPATH, "//input[@checked='checked']")
            gender_value = selected_gender_element.get_attribute('value')

            gender = '女性'
            if gender_value == 'M':
                gender = '男性'
            else:
                gender = '女性'

            selected_possible_customers_element = table_tr_datas[3].find_element(By.XPATH, "//option[@selected='selected']")
            possible_customers = selected_possible_customers_element.get_attribute('value')

            order_element = table_tr_datas[4].find_element(By.TAG_NAME, "input")
            order = order_element.get_attribute('value')

--------------------------------------------------------------------------------------------

            res_data = {
                "salon_id"      : str(salon_id),
                "name"            : name,
                "name_furi"       : name_kana,
                "profile"         : '',
                "nomination_fee"  : 0,
                "avatar"          : '',
                "possible_customers" : possible_customers,
                "nomination_reservation": '',
                "order"           : order,
                "business_time_response": business_time_response,
                "custom_time_response": '',
                "special_leave"   : special_leave
            }
            

            # update_and_register_staff_for_one_salon(json_data=json.dumps(res_data))

        except Exception as e:
            print(e)

        time.sleep(1)
        



    driver.quit()


def scrape_staff_thread():
    while 1:
        scrape_and_register_staff_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_staff_thread)
    my_thread.start()
    my_thread.join()
