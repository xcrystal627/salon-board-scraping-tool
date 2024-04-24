import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from datetime import  datetime 
from retrying import retry
from bs4 import BeautifulSoup
import threading
import time
import urllib
from urllib.parse import urlparse, parse_qs
import json
import re
from reservation_api import get_all_reservation_information_of_all_salon, get_unregistered_reservations
from salon_api import get_all_salon_information
from utils import convert_year_month_day_to_string, convert_time_to_string, get_current_time_as_YmdHMS_type
from salonboard_login import login_salonboard
from start_web_driver import start_driver




SHORT_WAIT_TIME = 3
MID_WAIT_TIME = 5
LONG_WAIT_TIME = 10


def read_reservation_from_db_register_to_salonboard():

    all_salons = get_all_salon_information() # get request to middle server for all salons
    
    for salon in all_salons:
        unregistered_reservations = get_unregistered_reservations(salon['id'])

        if len(unregistered_reservations) == 0:
            return
        
        driver = start_driver()
        if driver == None:
            print('While starting driver, occur error')    
            return
        
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        for reservation in unregistered_reservations:
            register_reservation_to_salonboard(driver, reservation)
        


def register_reservation_to_salonboard(driver, reservation):
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "headerNavigationBar"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    driver.get('https://salonboard.com/KLP/schedule/salonSchedule/')
    
    
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "schedule"))
        )
    except TimeoutError as e:
        driver.quit()
        return
    
    # reservation headers
    headerElement = driver.find_element(By.CSS_SELECTOR, 'div.scheduleMainHeadFrame.jscScheduleMainHeadFrame')
    staffList =  headerElement.find_element(By.CSS_SELECTOR, 'ul.scheduleMainHeadList.isStaff')
    staffs = staffList.find_elements(By.CSS_SELECTOR, 'li.scheduleMainHead')
    
    for i in range(len(staffs)):
        staff_reservation_page_link =  staffs[i].find_element(By.CSS_SELECTOR, 'a.scheduleLink')
        staff_name = staff_reservation_page_link.text
        print(staff_name)

        if staff_name != reservation['staff']:
            continue
        
        staff_reservation_page_link.click()
        time.sleep(SHORT_WAIT_TIME)
        
        parsed_url = urlparse(driver.current_url)
        staff_id = parse_qs(parsed_url.query).get('staffId', [''])[0]
        
        #  open register reservation page
        driver = enter_register_panel(driver=driver, staffid=staff_id, date=reservation['date'], start_time=reservation['start_time'])

        time.sleep(SHORT_WAIT_TIME)
        # input reservation parameters in input field
        input_reservation_parameters_input_fields(driver=driver, reservation=reservation)
        
        # update reservation is_registered status from false to true
         
        

def enter_register_panel(driver, staffid, date, start_time):

    converted_reservation_date = date.replace("-", "")
    hour = start_time.split(":")[0]
    minute = start_time.split(":")[1]

    last_update = get_current_time_as_YmdHMS_type()

    if last_update == None:
        driver.quit()
        return

    driver.get(f'https://salonboard.com/KLP/reserve/ext/extReserveRegist/?staffId={staffid}&date={converted_reservation_date}&rsvHour={hour}&rsvMinute={minute}&rlastupdate={last_update}')

    return driver



def input_reservation_parameters_input_fields( driver, reservation):

    reservation_required_time = reservation['required_time']
    reservation_required_split_time = reservation_required_time.split(":")

    reservation_required_hour = reservation_required_split_time[0]
    reservation_required_minute = reservation_required_split_time[1]

    required_time_hour_element = driver.find_element(By.ID, 'jsiRsvTermHour')
    select_required_hour = Select(required_time_hour_element)
    select_required_hour.select_by_visible_text(reservation_required_hour)

    time.sleep(1)

    required_time_minute_element = driver.find_element(By.ID, 'jsiRsvTermMinute')
    select_required_minute = Select(required_time_minute_element)
    select_required_minute.select_by_visible_text(reservation_required_minute)

    time.sleep(1)

    reservation_route = reservation['reservation_route']

    reservation_route_element = driver.find_element(By.XPATH, '//select[@name="rsvRouteId"]')
    select_reservation_route = Select(reservation_route_element)
    select_reservation_route.select_by_visible_text(reservation_route)

    time.sleep(1)
    




    pass





def read_register_thread():
    # while 1:
        read_reservation_from_db_register_to_salonboard()
        # time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=read_register_thread)
    my_thread.start()
    my_thread.join()

