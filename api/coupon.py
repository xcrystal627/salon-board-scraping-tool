import requests
import dotenv
import json
import base64 


def get_coupons_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.get(f'{glot_middle_server_url}api/coupon/{user_id}', headers=headers)

    coupons = []
    
    if response.status_code == 200:
        coupons = response.json()['coupons']
        print("GET request successful!")
    else:
        print( response.json()['message'])
    
    return coupons
    


def register_coupon_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.post(f'{glot_middle_server_url}api/coupon/new', data=json_data, headers=headers)
    
    
    if response.status_code == 200:
        print(response.json())
        print("Register new coupon request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def update_and_register_coupon_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.post(f'{glot_middle_server_url}api/coupon/update', data=json_data, headers=headers)    
    
    if response.status_code == 200:
        print(response.json())
        print("Update new coupon request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def delete_coupons_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/coupon/{user_id}', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:        
        print( response.json()['message'])

    


def delete_all_coupons_for_all_salon():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/coupon/all', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:
        print( response.json()['message'])

