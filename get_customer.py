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
from api.customer import update_and_register_customer_for_one_salon




SHORT_WAIT_TIME = 2
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5



def scrape_and_register_customer_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons

    
    for salon in all_salons:
        driver = start_driver()

        if driver == None:
            print('While starting driver, occur error')    
            return
            
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_customer_from_saloboard(driver, salon['id'])



def get_customer_from_saloboard(driver, salon_id):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/KLP/customer/customerSearch/')

    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "search"))
        )   
    except TimeoutError as e:
        driver.quit()
        return
    
    search_button_element = driver.find_element(By.ID, 'search')
    search_button_element.click()

    while True:

        customer_table = driver.find_element(By.CSS_SELECTOR, 'table.customerInfoTbl')    
        
        customer_table_trs = customer_table.find_elements(By.TAG_NAME, 'tr')
        customer_count = len(customer_table_trs) - 1

        current_url = driver.current_url    

        thread_count = int(customer_count / 5)


        for idx in range(0, thread_count ):
            
            threads = []
            for j in range(1, 6):
                order = idx * 5 + j
                print(order)
                if order > customer_count: continue

                my_thread = threading.Thread(target=get_customer_information, args=(driver, salon_id, current_url, order,))
                threads.append(my_thread) 

            for item in threads:
                item.start()
                item.join()

            time.sleep(1)

        driver.get(current_url)
        
        if customer_count == 50:
            next_page_link = driver.find_element(By.XPATH, "//div[@class='columnBlock02']//div[@class='paging']//p[@class='next']//a")
            next_page_link.click()
            time.sleep(1)
        else:
            break

    driver.quit()


def get_customer_information(driver, salon_id, current_url, order):
    driver.get(current_url)
    customer_table = driver.find_element(By.CSS_SELECTOR, 'table.customerInfoTbl')    
    
    customer_table_trs = customer_table.find_elements(By.TAG_NAME, 'tr')
    detail_link = customer_table_trs[order].find_element(By.CSS_SELECTOR, 'a.customerActionLinkTypePost')
    detail_link.click()

    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "customerDetail"))
        )   
    except TimeoutError as e:
        driver.quit()
        return
    
    try:
        tables = driver.find_elements(By.TAG_NAME, 'table')

        first_table_trs = tables[0].find_elements(By.TAG_NAME, 'tr')
        customer_name_kanji = first_table_trs[0].find_element(By.TAG_NAME, 'td').text
        customer_name_kana = first_table_trs[1].find_element(By.TAG_NAME, 'td').text
        customer_phone_one = first_table_trs[2].find_element(By.TAG_NAME, 'td').text
        customer_phone_two = first_table_trs[3].find_element(By.TAG_NAME, 'td').text

        customer_phone = ''
        if customer_phone_one != '-':
            customer_phone = customer_phone_one
        elif customer_phone_two != '-':
            customer_phone = customer_phone_two


        customer_email_pc = first_table_trs[4].find_element(By.TAG_NAME, 'td').text
        customer_email_mobile = first_table_trs[5].find_element(By.TAG_NAME, 'td').text

        customer_email = ''
        if customer_email_pc != '-':
            customer_email = customer_email_pc
        elif customer_email_mobile != '-':
            customer_email = customer_email_mobile


        second_table_trs = tables[1].find_elements(By.TAG_NAME, 'tr')
        customer_birth_date = second_table_trs[0].find_element(By.TAG_NAME, 'td').text
        customer_gender = second_table_trs[1].find_element(By.TAG_NAME, 'td').text
        customer_note = second_table_trs[5].find_element(By.TAG_NAME, 'td').text

        fourth_table_trs = tables[3].find_elements(By.TAG_NAME, 'tr')
        customer_route = fourth_table_trs[0].find_element(By.TAG_NAME, 'td').text

        print(customer_name_kana, customer_name_kanji, customer_email, customer_gender, customer_phone, customer_birth_date, customer_route, customer_note)
                
        res_data = {
            "salon_id"      : str(salon_id),
            "name_kanji"    : customer_name_kanji,
            "name_kana"     : customer_name_kana,
            "gender"        : customer_gender,
            "birth_date"    : customer_birth_date,
            "phone"         : customer_phone,
            "email"         : customer_email,
            "note"          : customer_note,
            "route"         : customer_route            
        }
        
        update_and_register_customer_for_one_salon(json_data=json.dumps(res_data))



    except Exception as error:
        print('Error getting customer information')
       


def scrape_customer_thread():
    while 1:
        scrape_and_register_customer_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_customer_thread)
    my_thread.start()
    my_thread.join()