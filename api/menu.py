import requests
import dotenv
import json
import base64 


def get_menu_items_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.get(f'{glot_middle_server_url}api/menu/{user_id}', headers=headers)

    menu_items = []
    
    if response.status_code == 200:
        menu_items = response.json()['menus']
        print("GET request successful!")
    else:
        print( response.json()['message'])
    
    return menu_items
    


def register_menu_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.post(f'{glot_middle_server_url}api/menu/new', data=json_data, headers=headers)
    
    
    if response.status_code == 200:
        print(response.json())
        print("Register new menu item request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def update_and_register_menu_item_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.post(f'{glot_middle_server_url}api/menu/update', data=json_data, headers=headers)    
    
    if response.status_code == 200:
        print(response.json())
        print("Update new menu request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def delete_menu_items_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/menu/{user_id}', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:        
        print( response.json()['message'])

    


def delete_all_menu_items_for_all_salon():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/menu/all', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:
        print( response.json()['message'])

