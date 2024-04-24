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
from utils import convert_year_month_day_to_string, convert_time_to_string
from salonboard_login import login_salonboard
from start_web_driver import start_driver




SHORT_WAIT_TIME = 1
MID_WAIT_TIME = 3
LONG_WAIT_TIME = 5




def scrape_and_register_reservation_to_middle_db():

    all_salons = get_all_salon_information() # get request to middle server for all salons

    
    for salon in all_salons:
        driver = start_driver()

        if driver == None:
            print('While starting driver, occur error')    
            return
            
        driver = login_salonboard(driver, salon['user_id'], salon['password'])
        get_schedule_for_salon(driver, salon['id'])




def get_schedule_for_salon(driver, salon_id):

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
    
        headerElement = driver.find_element(By.CSS_SELECTOR, 'div.scheduleMainHeadFrame.jscScheduleMainHeadFrame')
        staffList =  headerElement.find_element(By.CSS_SELECTOR, 'ul.scheduleMainHeadList.isStaff')
        staffs = staffList.find_elements(By.CSS_SELECTOR, 'li.scheduleMainHead')

        staff_reservation_page_link =  staffs[i].find_element(By.CSS_SELECTOR, 'a.scheduleLink')
        WebDriverWait(driver, SHORT_WAIT_TIME)
        staff_reservation_page_link.click()

        try:
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.scheduleMainTable"))
            )
        except TimeoutError as e:
            driver.quit()
            return
        
        get_week_schedule(driver, salon_id)
        
        # scrape the next week schedule-------------------------------------------------------------------------------
       
        for i in range(12):
            
            time.sleep(SHORT_WAIT_TIME)
            scheduleCalenderDayList  =  driver.find_elements(By.CSS_SELECTOR, 'li.scheduleCalenderDay')
            
            nextDayLink = None

            try:
                nextDayLink =  scheduleCalenderDayList[9].find_element(By.CSS_SELECTOR, 'a')
            except Exception as error:
                print('Can not find next day link(9)')

            
            if nextDayLink == None:
                try:
                    nextDayLink =  scheduleCalenderDayList[10].find_element(By.CSS_SELECTOR, 'a')
                except Exception as error:
                    print('Can not find next day link(10)')

            if nextDayLink == None:    
                try:
                    nextDayLink =  scheduleCalenderDayList[11].find_element(By.CSS_SELECTOR, 'a')
                except Exception as error:
                    print('Can not find next day link(11)')
                    return

            driver.execute_script("arguments[0].click();", nextDayLink)
            time.sleep(SHORT_WAIT_TIME)

            get_week_schedule(driver, salon_id)





def get_week_schedule(driver, salon_id):
        

    for i in range(7):
        weekScheduleList = driver.find_elements(By.CSS_SELECTOR, "li.scheduleMainTableLine")
        scheduleDayList = driver.find_elements(By.CSS_SELECTOR, "li.scheduleMainHead")

        # print(i, " week range: ", weekScheduleList)
        try:
            # scheduleToDoList = []
            
            # try:
            #     scheduleToDoList =  weekScheduleList[i].find_elements(By.CSS_SELECTOR, 'div.scheduleToDo')
            # except Exception as error:
            #     print("Not exist scheduleToDoList")

            # if len(scheduleToDoList) > 0:
            #     print('Schedule to do list ----------------------------------------------------')
            #     for j in range(len(scheduleToDoList)):
                    
            #         try:
            #             timeToDoItemElement = scheduleToDoList[j].find_element(By.CSS_SELECTOR, 'p.scheduleTimeZoneSetting')
            #             timeToDoItemElementHTMLContent = timeToDoItemElement.get_attribute("outerHTML")
            #             item = BeautifulSoup(timeToDoItemElementHTMLContent, "html.parser")
            #             displayTime = item.text
            #             start_end_times = displayTime[1:-1].split(',')
            #             start_time = start_end_times[0][1:-1]
            #             end_time = start_end_times[1][2:-1]
            #             reservation_date = scheduleDayList[i].text
                        
            #             res_data = {
            #                 "salon_id": str(salon_id),
            #                 "menu_item": "",
            #                 "date": convert_year_month_day_to_string(reservation_date),
            #                 "start_time": convert_time_to_string(start_time),
            #                 "end_time": convert_time_to_string(end_time),
            #                 "staff": "",
            #                 "nomination": "",
            #                 "customer_name": "",
            #                 "customer_phone": "",
            #                 "customer_note": "",
            #                 "end_notification": "",
            #                 "coupon": "",
            #                 "reservation_route": "",
            #                 "required_time": "",
            #                 "staff_start_time": "",
            #                 "staff_end_time": "",
            #                 "facility_name": "",
            #                 "facility_start_time": "",
            #                 "facility_end_time": ""
            #             }

            #             print('already scheduled: ', start_time, end_time)
            #         except Exception as error:
            #             print("scheduleTodoList : ", error)

            #         try:
            #             response_message = update_register_reservation(json.dumps(res_data))
            #             print(response_message)
            #         except Exception as error:
            #             print(error)

            #         time.sleep(SHORT_WAIT_TIME)

            scheduleReservationList = []

            try:
                scheduleReservationList =  weekScheduleList[i].find_elements(By.CSS_SELECTOR, 'div.scheduleReservation')
            except Exception as error:
                print("Not exist scheduleReservationList")        

            if len(scheduleReservationList) > 0:
                print('Schedule reservation list ===============================================')
                time.sleep(SHORT_WAIT_TIME)
                for k in range(len(scheduleReservationList)):
                    
                    _weekScheduleList = driver.find_elements(By.CSS_SELECTOR, "li.scheduleMainTableLine")
                    _scheduleReservationList =  _weekScheduleList[i].find_elements(By.CSS_SELECTOR, 'div.scheduleReservation')
                    _scheduleReservationList[k].click()

                    popupElement = driver.find_element(By.CSS_SELECTOR, 'div.mod_popup_02')
                    detailButtonElement =  popupElement.find_element(By.XPATH, '//a[contains(text(),"詳細")]')
                    time.sleep(SHORT_WAIT_TIME)
                    driver.execute_script("arguments[0].click();", detailButtonElement)
                    time.sleep(SHORT_WAIT_TIME)

                    reservationType = ''

                    try:
                        form = driver.find_element(By.ID, 'extReserveDetail')
                        reservationType = 'extReserveDetail'
                    except Exception as error:
                        print('Not extReserveDetail')

                    try:
                        form = driver.find_element(By.ID, 'netReserveDetail')
                        reservationType = 'netReserveDetail'
                    except Exception as error:
                        print('Not netReserveDetail')


                    if reservationType == 'netReserveDetail':
                        print('netReserveDetail ++++++++++++++++++++++++++++++++++++++++++++++++')
                        tables = driver.find_elements(By.CSS_SELECTOR, 'table.mod_table03')

                        reservation_number = tables[0].find_element(By.CSS_SELECTOR, 'td.w277').text

                        reservation_time = tables[1].find_element(By.XPATH, "//p[@id='rsvDate']")

                        reservationTimeElementHTMLContent = reservation_time.get_attribute("outerHTML")
                        reservationTimeItem = BeautifulSoup(reservationTimeElementHTMLContent, "html.parser")
                        reservationTimeText = reservationTimeItem.text
                        reservationTimeText.replace(' ', '').replace('\t', '').replace('\n', '')  
                        reservatinoDateValue =  reservationTimeText.split('\uff5e')
                        reservation_date_start_time = reservatinoDateValue[0].replace(' ', '').replace('\t', '').replace('\n', '').split('年')[1]
                        reservation_year = reservatinoDateValue[0].replace(' ', '').replace('\t', '').replace('\n', '').split('年')[0]
                        reservation_month_day = reservation_date_start_time.split('\uFF08')[0]
                        reservation_date = convert_year_month_day_to_string(reservation_year, reservation_month_day)

                        start_time = reservation_date_start_time.split('\uff09')[1]
                        end_time = reservatinoDateValue[1].replace(' ', '').replace('\t', '').replace('\n', '')[:5]
                        
                        required_time = datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")
                        required_time = str(required_time)[:4]
        
                        # print('date: ', reservation_date, 'start_time: ', start_time, 'end_time: ', end_time)

                        reservation_table_trs = tables[1].find_elements(By.CSS_SELECTOR, 'tr.mod_left')
                        
                        reservation_route = ''
                        menu_item = ''
                        coupon = ''

                        # reservation_route menu_item coupon ---------------------------------------------------------------------------------------------
                        for idx in range(len(reservation_table_trs)):
                            row_header = reservation_table_trs[idx].find_element(By.TAG_NAME, 'th').text
                            
                            if row_header == '予約経路':
                                reservation_route = reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                            elif row_header == 'メニュー':
                                menu_item = reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                            elif row_header == 'クーポン名':                
                                coupon = reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                            

                        staff_facility_table_trs = tables[2].find_elements(By.CSS_SELECTOR, 'tr.mod_left')
                        staff = staff_facility_table_trs[0].find_element(By.XPATH, 'td//table//tbody//tr//td[1]//div').text
                        staff_time_start_end = staff_facility_table_trs[0].find_element(By.XPATH, 'td//table//tbody//tr//td[2]').text
                        staff_start_time = staff_time_start_end.replace(" ", '').split('\uff5e')[0]
                        staff_end_time = staff_time_start_end.replace(" ", '').split('\uff5e')[1]
                        nomination = False

                        # print('staff', staff,'staff_start_time: ', staff_start_time,'staff_end_time' , staff_end_time)

                        try:
                            nomination_sign =  staff_facility_table_trs[1].find_element(By.XPATH, '//td//table//tbody//tr//td[3]//div')
                            if nomination_sign is not None:  
                                nomination = True
                        except Exception as error:
                            print(error)
                            nomination = False

                        # print('staff_facility_table_trs: ', staff_facility_table_trs[0].text, staff_facility_table_trs[1].text )
                        
                        facility_name = ''
                        facility_start_time = ''
                        facility_end_time = ''

                        try:
                            facility_name = staff_facility_table_trs[1].find_element(By.XPATH, 'td//table//tbody//tr//td[1]//div').text
                            facility_time_start_end = staff_facility_table_trs[1].find_element(By.XPATH, 'td//table//tbody//tr//td[2]').text
                            facility_start_time = facility_time_start_end.replace(" ", '').split('\uff5e')[0]
                            facility_end_time = facility_time_start_end.replace(" ", '').split('\uff5e')[1]
                        except Exception as error:
                            print(error)
                            print('Not found facility information')

                        # print('facility_name: ', facility_name, 'facility_start_time: ', facility_time_start_end, 'facility_end_time: ', facility_end_time)                        
                        
                        customer_name = tables[4].find_element(By.CSS_SELECTOR, 'div.nameKana').text
                        customer_table_trs = tables[4].find_elements(By.CSS_SELECTOR, 'tr.mod_left')
                        customer_phone = customer_table_trs[2].find_element(By.TAG_NAME, 'td').text
                        customer_note = customer_table_trs[5].find_element(By.XPATH, 'td').text
                        print(customer_name, customer_phone, customer_note)
                                               
                        res_data = {
                            "salon_id": str(salon_id),
                            "menu_item": menu_item,
                            "reservation_number": reservation_number,
                            "date": reservation_date,
                            "start_time": convert_time_to_string(start_time),
                            "end_time": convert_time_to_string(end_time),
                            "staff": staff,
                            "nomination": nomination,
                            "customer_name": customer_name,
                            "customer_phone": customer_phone,
                            "customer_note": customer_note,
                            "end_notification": "",
                            "coupon": coupon,
                            "reservation_route": reservation_route,
                            "required_time": required_time,
                            "staff_start_time": staff_start_time,
                            "staff_end_time": staff_end_time,
                            "facility_name": facility_name,
                            "facility_start_time": facility_start_time,
                            "facility_end_time": facility_end_time
                        }

                        try:
                            response_message = update_register_reservation(json.dumps(res_data))
                            print(response_message)
                        except Exception as error:
                            print(error)
                        
                        time.sleep(SHORT_WAIT_TIME)
                        driver.back()
                        time.sleep(SHORT_WAIT_TIME)

                    elif reservationType == 'extReserveDetail':
                        print('extReserveDetail --------------------------------------------')

                        tables = driver.find_elements(By.CSS_SELECTOR, 'table.mod_table03')

                        reservation_number = tables[0].find_element(By.CSS_SELECTOR, 'td.w277').text
                        print(reservation_number,'========================================')

                        reservation_time = tables[1].find_element(By.XPATH, "//p[@id='rsvDate']")

                        reservationTimeElementHTMLContent = reservation_time.get_attribute("outerHTML")
                        reservationTimeItem = BeautifulSoup(reservationTimeElementHTMLContent, "html.parser")
                        reservationTimeText = reservationTimeItem.text
                        
                        reservationTimeText.replace(' ', '').replace('\t', '').replace('\n', '')  
                        reservatinoDateValue =  reservationTimeText.split('\uff5e')
                        reservation_date_start_time = reservatinoDateValue[0].replace(' ', '').replace('\t', '').replace('\n', '').split('年')[1]
                        
                        reservation_year = reservatinoDateValue[0].replace(' ', '').replace('\t', '').replace('\n', '').split('年')[0]
                        reservation_month_day = reservation_date_start_time.split('\uFF08')[0]
                        reservation_date = convert_year_month_day_to_string(reservation_year, reservation_month_day)
                        
                        start_time = reservation_date_start_time.split('\uff09')[1]
                        end_time = reservatinoDateValue[1].replace(' ', '').replace('\t', '').replace('\n', '')[:5]

                        required_time = datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")
                        required_time = str(required_time)[:4]

                        reservation_table_trs = tables[1].find_elements(By.CSS_SELECTOR, 'tr.mod_left')
                        
                        reservation_route = ''
                        menu_item = ''
                        coupon = ''


                        # reservation_route menu_item coupon ---------------------------------------------------------------------------------------------
                        for idx in range(len(reservation_table_trs)):
                            try:
                                row_header = reservation_table_trs[idx].find_element(By.TAG_NAME, 'th').text
                            
                                if row_header == '予約経路':
                                    reservation_route = reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                                elif row_header == 'メニュー':
                                    menu_item = reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                                    pass
                                elif row_header == 'クーポン名':                
                                    coupon = reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                            except Exception as error:
                                print('Not find th')
                                menu_item = menu_item + "&&" + reservation_table_trs[idx].find_element(By.CSS_SELECTOR, 'td').text
                            


                        staff_facility_table_trs = tables[2].find_elements(By.CSS_SELECTOR, 'tr.mod_left')
                        staff = staff_facility_table_trs[0].find_element(By.XPATH, 'td//table//tbody//tr//td[1]//div').text
                        staff_time_start_end = staff_facility_table_trs[0].find_element(By.XPATH, 'td//table//tbody//tr//td[2]//div').text
                        staff_start_time = staff_time_start_end.replace(" ", '').split('\uff5e')[0]
                        staff_end_time = staff_time_start_end.replace(" ", '').split('\uff5e')[1]
                        nomination = False

                        # print('staff ', staff,'staff_start_time: ', staff_start_time,'staff_end_time' , staff_end_time)

                        print(menu_item)

                        try:
                            nomination_sign =  staff_facility_table_trs[1].find_element(By.XPATH, '//td//table//tbody//tr//td[3]')
                            if nomination_sign is not None:  
                                nomination = True
                        except Exception as error:
                            print(error)
                            nomination = False

                        # print('staff_facility_table_trs: ', staff_facility_table_trs[0].text, staff_facility_table_trs[1].text )

                        facility_name = ''
                        facility_start_time = ''
                        facility_end_time = ''

                        try:
                            facility_name = staff_facility_table_trs[1].find_element(By.XPATH, 'td//table//tbody//tr//td[1]//div').text
                            facility_time_start_end = staff_facility_table_trs[1].find_element(By.XPATH, 'td//table//tbody//tr//td[2]').text
                            facility_start_time = facility_time_start_end.replace(" ", '').split('\uff5e')[0]
                            facility_end_time = facility_time_start_end.replace(" ", '').split('\uff5e')[1]
                        except Exception as error:
                            print(error)
                            print('Not found facility information')


                        # print('date: ', reservation_date, 'start_time: ', start_time, 'end_time: ', end_time)
                        
                        # print('nomination: ', nomination,  'facility_name: ', facility_name, 'facility_start_time: ', facility_time_start_end, 'facility_end_time: ', facility_end_time)                        

                        customer_name = tables[3].find_element(By.CSS_SELECTOR, 'div.nameKana').text
                        customer_table_trs = tables[3].find_elements(By.CSS_SELECTOR, 'tr.mod_left')
                        customer_phone = customer_table_trs[2].find_element(By.TAG_NAME, 'td').text
                        customer_note = customer_table_trs[5].find_element(By.XPATH, 'td').text
                        # print(customer_name, customer_phone, customer_note)


              
                        res_data = {
                            "salon_id": str(salon_id),
                            "menu_item": menu_item,
                            "reservation_number": reservation_number,
                            "date": reservation_date,
                            "start_time": convert_time_to_string(start_time),
                            "end_time": convert_time_to_string(end_time),
                            "staff": staff,
                            "nomination": nomination,
                            "customer_name": customer_name,
                            "customer_phone": customer_phone,
                            "customer_note": customer_note,
                            "end_notification": "",
                            "coupon": coupon,
                            "reservation_route": reservation_route,
                            "required_time": required_time,
                            "staff_start_time": staff_start_time,
                            "staff_end_time": staff_end_time,
                            "facility_name": facility_name,
                            "facility_start_time": facility_start_time,
                            "facility_end_time": facility_end_time
                        }

                        try:
                            response_message = update_register_reservation(json.dumps(res_data))
                            print(response_message)
                        except Exception as error:
                            print(error)

                        time.sleep(SHORT_WAIT_TIME)
                        driver.back()
                        time.sleep(SHORT_WAIT_TIME) 
                        
            
        except Exception as error:
            print(error)
            print('Schedule Nothing')
        



def scrape_register_thread():
    while 1:
        scrape_and_register_reservation_to_middle_db()
        time.sleep(60*10)




if __name__ == "__main__":
    my_thread = threading.Thread(target=scrape_register_thread)
    my_thread.start()
    my_thread.join()

