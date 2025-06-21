import os
import time
import requests
from datetime import datetime
import os
import requests
health_Timeout = 1
def get_stations(offset=0, limit=0, search=""):
    url = f"{os.getenv('API_URL')}/stations"

    params = {
        'offset': offset,
        'limit': limit,
    }
    if search:
        params['search'] = search

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[get_stations] {e}")
        return []

def get_users():
    url = f"{os.getenv('API_URL')}/users"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[get_users] {e}")
        return []
    
def get_user_by_email(email):
    url = f"{os.getenv('API_URL')}/users/by-email/{email}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[get_user] {e}")
        return []
    
def create_user(newUser):
    url = f"{os.getenv('API_URL')}/users"
    try:
        response = requests.post(url, json=newUser)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[create_user] {e}")
        return None
    
def patch_user_by_id(user_id, json_data):
    url = f"{os.getenv('API_URL')}/users/{user_id}"
    try:
        response = requests.patch(url, json=json_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[patch_user_by_id] {e}")
        return None

def activate_user(email):
    user = get_user_by_email(email)
    if user and not user.get('is_active', False): 
        return patch_user_by_id(user.get('id'), {"is_active": True})
    return None

def fetch_IOT():
    results = []
    try:
        response = requests.get(os.getenv('API_URL')+"/iot/1")
        response.raise_for_status()
        results.append(response.json())
    except requests.RequestException as e:
        print(f"[fetch_IOT] {e}")
        return []
    try:
        response = requests.get(os.getenv('API_URL')+"/iot/2")
        response.raise_for_status()
        results.append(response.json())
    except requests.RequestException as e:
        print(f"[fetch_IOT] {e}")
        return []
    return results

def get_user_service_health():
    try:
        response = requests.get(os.getenv('API_URL')+"/health/users", timeout=health_Timeout)
        response.raise_for_status()
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"[get_user_service_health] {e}")
        return False
    
def get_station_service_health():
    try:
        response = requests.get(os.getenv('API_URL')+"/health/stations", timeout=health_Timeout)
        response.raise_for_status()
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"[get_station_service_health] {e}")
        return False
    
    
