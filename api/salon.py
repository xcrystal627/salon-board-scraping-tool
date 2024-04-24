import requests
import dotenv
import json
import base64


def get_all_salon_information():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.get(f'{glot_middle_server_url}api/salon/all', headers=headers)


    salons = []
    salon_info = []
    
    if response.status_code == 200:
        salons = response.json()['salons']
        

        for salon in salons:
            decoded_text = base64.b64decode(salon['password'])
            decoded_password = decoded_text.decode('utf-8')

            item = {
                'id'        : salon['id'],
                'user_id'   : salon['user_id'],
                'password'  : decoded_password
            }
            
            salon_info.append(item)

        print("GET request successful!")
    else:
        print( response.json()['message'])
    
    return salon_info
    


def get_one_salon_information(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.get(f'{glot_middle_server_url}api/salon/{user_id}', headers=headers)

    salon_info = {}
    
    if response.status_code == 200:
        salons = response.json()['salon']
        print("GET request successful!")
    else:
        print( response.json()['message'])
    
    return salon_info
    

def delete_one_salon_information(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/salon/{user_id}', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:        
        print( response.json()['message'])

    
    


def delete_all_salon_information():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/salon/all', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:
        print( response.json()['message'])

