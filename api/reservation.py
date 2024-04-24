
import requests
import dotenv
import json
import base64





def update_register_reservation(json_data):

    # salon_id, menu_item, date, start_time, end_time, staff, nomination, customer_name, customer_phone, customer_note, end_notification, 
    #             coupon, reservation_route, required_time, staff_start_time, staff_end_time, facility_name, facility_start_time, facility_end_time


    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']


    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.post(f'{glot_middle_server_url}api/reservation/update_register', data=json_data, headers=headers)

    if response.status_code == 200:
        print(response.json())
        print("Register new reservation request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']




def get_all_reservation_information_of_one_salon(salon_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.get(f'{glot_middle_server_url}api/reservation/{salon_id}', headers=headers)
    
    reservations = []

    if response.status_code == 200:
        reservations = response.json()['reservations']
        print("GET request successful!")
        print(response.json()['message'])
    else:
        print("GET request failed.")
        print(response.json()['message'])
        
    return reservations 


def get_all_reservation_information_of_all_salon():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.get(f'{glot_middle_server_url}api/reservation/all', headers=headers)


    reservations = []

    if response.status_code == 200:
        reservations = response.json()['reservations']
        print("GET request successful!")
        print(response.json()['message'])
    else:
        print("GET request failed.")
        print(response.json()['message'])
        
    return reservations



def get_unregistered_reservations(salon_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.get(f'{glot_middle_server_url}api/reservation/unregistered/{salon_id}', headers=headers)


    reservations = []

    if response.status_code == 200:
        reservations = response.json()['reservations']
        print("GET request successful!")
        print(response.json()['message'])
    else:
        print("GET request failed.")
        print(response.json()['message'])
        
    return reservations




def delete_all_reservation_of_one_salon(salon_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.delete(f'{glot_middle_server_url}api/reservation/{salon_id}', headers=headers)

    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(  response.json()['message'])



def delete_all_reservation_of_all_salon():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.delete(f'{glot_middle_server_url}api/reservation/all', headers=headers)

    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(  response.json()['message'])





