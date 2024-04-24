import requests
import dotenv
import json
import base64 


def get_facilities_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.get(f'{glot_middle_server_url}api/facility/{user_id}', headers=headers)

    facilities = []
    
    if response.status_code == 200:
        facilities = response.json()['facilities']
        print("GET request successful!")
    else:
        print( response.json()['message'])
    
    return facilities
    


def register_facility_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.post(f'{glot_middle_server_url}api/facility/new', data=json_data, headers=headers)
    
    
    if response.status_code == 200:
        print(response.json())
        print("Register new facility request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def update_and_register_facility_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.post(f'{glot_middle_server_url}api/facility/update', data=json_data, headers=headers)    
    
    if response.status_code == 200:
        print(response.json())
        print("Update new facility request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def delete_facilities_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/facility/{user_id}', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:        
        print( response.json()['message'])

    


def delete_all_facilities_for_all_salon():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/facility/all', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:
        print( response.json()['message'])

