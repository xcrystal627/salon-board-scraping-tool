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



MOMENT_WAIT_TIME = 0.5
ONE_WAIT_TIME = 1
SHORT_WAIT_TIME = 2
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5



def scrape_and_register_coupon_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons
    driver = start_driver()

    if driver == None:
        print('While starting driver, occur error')    
        return
    
    for salon in all_salons:
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_coupon_from_saloboard(driver, salon['id'])



def get_coupon_from_saloboard(driver, salon_id):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/CNK/draft/couponList/')

    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.table_list_store'))
        )
    except TimeoutError as e:
        print(e)
        driver.quit()
        return

    # display_menu_set_tables = driver.find_elements(By.XPATH, '//table[@style="display: table;" and (contains(@class, "menuSetTable"))]')
     
    _coupon_table = driver.find_element(By.CSS_SELECTOR, 'table.table_list_store')
    _table_trs = _coupon_table.find_elements(By.TAG_NAME, 'tr')

    for idx in range(len(_table_trs)):

        try:
            coupon_table = driver.find_element(By.CSS_SELECTOR, 'table.table_list_store')
            table_trs = coupon_table.find_elements(By.TAG_NAME, 'tr')

            if idx == 0 or idx == 1:
                continue
            tr_tds = table_trs[idx].find_elements(By.TAG_NAME, 'td')
            a_detail_tag = tr_tds[6].find_element(By.TAG_NAME, 'a')
            a_detail_tag.click()

            time.sleep(ONE_WAIT_TIME)
            coupon_edit_table = driver.find_element(By.CSS_SELECTOR, '.table_edit_store.storeCouponEditTable')
            coupon_edit_table_trs = coupon_edit_table.find_elements(By.TAG_NAME, 'tr')

            coupon_type_tds = coupon_edit_table_trs[1].find_elements(By.TAG_NAME, 'td')
            
            coupon_type = coupon_type_tds[0].find_element(By.XPATH, '//option[@selected="selected"]').text

            coupon_name = coupon_edit_table_trs[2].find_element(By.XPATH, '//input[@name="frmCouponEditDto.couponName"]').get_attribute('value')

            coupon_description = coupon_edit_table_trs[3].find_element(By.XPATH, '//textarea[@name="frmCouponEditDto.contentExplanation"]').get_attribute('value')
            
            print(coupon_description, coupon_type, coupon_name)

            driver.back()
            time.sleep(ONE_WAIT_TIME)
        except Exception as error:
            print(error)



    driver.quit()


def scrape_coupon_thread():
    while 1:
        scrape_and_register_coupon_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_coupon_thread)
    my_thread.start()
    my_thread.join()
