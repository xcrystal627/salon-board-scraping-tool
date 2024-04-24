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
from api.reservation import update_register_reservation
from api.salon import get_all_salon_information
from api.reservation_route import register_reservation_route_for_one_salon, update_and_register_reservation_route_for_one_salon
from salonboard_login import login_salonboard
from start_web_driver import start_driver



SHORT_WAIT_TIME = 2
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5



def scrape_and_register_reservation_route_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons

    
    for salon in all_salons:
        driver = start_driver()

        if driver == None:
            print('While starting driver, occur error')    
            return

        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_reservation_route_from_saloboard(driver, salon['id'])



def get_reservation_route_from_saloboard(driver, salon_id):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/KLP/set/reserveRouteList/')

    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "rsvRouteSetup"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    reservation_route_table = driver.find_element(By.CSS_SELECTOR, "table.borderSupportForFirefox")
    table_rows = reservation_route_table.find_elements(By.CSS_SELECTOR, 'tr.mod_middle')
    
    for idx in range(len(table_rows)):
        if idx == 0 or idx == len(table_rows)-1:
            continue
        
        try:
            reservation_route_content = table_rows[idx].find_elements(By.CSS_SELECTOR, 'td')
            reservation_route_name = reservation_route_content[1].text
            reservation_route_description = reservation_route_content[3].text
            
            res_data = {
                "salon_id"      : str(salon_id),
                "route_name"    : reservation_route_name,
                "display_order" : idx,
                "description"   : reservation_route_description,
                "abbreviation"  : ''
                
            }
            

            update_and_register_reservation_route_for_one_salon(json_data=json.dumps(res_data))

        except Exception as e:
            print(e)

        time.sleep(1)

    driver.quit()


def scrape_reservation_route_thread():
    while 1:
        scrape_and_register_reservation_route_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_reservation_route_thread)
    my_thread.start()
    my_thread.join()
