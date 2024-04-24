import re
from datetime import datetime
import requests
import time


def convert_year_month_day_to_string(year ,display_date):
    
    match = re.search(r"\d+月\d+日", display_date)

    year_month_date = ''
    if match:
        date_string = match.group()
        year_month_date = str(datetime.strptime(year + date_string, "%Y%m月%d日").date())
       
    else:
        print("No date found in the string.")
    
    return year_month_date

    

    
def convert_time_to_string(time):

    converted_time = str(datetime.strptime(time, "%H:%M").time())[:5]
        

    return converted_time



def get_current_time_as_YmdHMS_type():
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Asia/tokyo')
    except Exception as error:
        print('network error')
        return None

    current_time_json = response.json()
    current_time = current_time_json['datetime']

    # Parse the string into a datetime object
    datetime_obj = datetime.fromisoformat(current_time)

    # Format the datetime object to get the desired value
    output_value = datetime_obj.strftime("%Y%m%d%H%M%S")

    return output_value

