import requests
import dotenv
import json
import base64 


def get_reservation_routes_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.get(f'{glot_middle_server_url}api/reservation_route/{user_id}', headers=headers)

    reservation_routes = []
    
    if response.status_code == 200:
        reservation_routes = response.json()['reservationRoutes']
        print("GET request successful!")
    else:
        print( response.json()['message'])
    
    return reservation_routes
    


def register_reservation_route_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }


    response = requests.post(f'{glot_middle_server_url}api/reservation_route/new', data=json_data, headers=headers)
    
    
    if response.status_code == 200:
        print(response.json())
        print("Register new reservation route request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def update_and_register_reservation_route_for_one_salon(json_data):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.post(f'{glot_middle_server_url}api/reservation_route/update', data=json_data, headers=headers)    
    
    if response.status_code == 200:
        print(response.json())
        print("Update new reservation route request successful!")
    else:
        print( response.json()['message'])

    return response.json()['message']



def delete_reservation_routes_for_one_salon(user_id):

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/reservation_route/{user_id}', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:        
        print( response.json()['message'])

    


def delete_all_reservation_routes_for_all_salon():

    auth_token = dotenv.dotenv_values('.env')['FIXED_TOKEN']
    glot_middle_server_url = dotenv.dotenv_values('.env')['GLOT_MIDDLE_SERVER_URL']

    headers = {
        "Authorization": f"{auth_token}",
        'Content-Type': 'application/json'
    }

    response = requests.delete(f'{glot_middle_server_url}api/reservation_route/all', headers=headers)
    
    if response.status_code == 200:
        print("Delete request successful!")
    else:
        print( response.json()['message'])

