import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_stations(offset=0, limit=100):
    url = f"{os.getenv('API_URL')}/stations"
    params = {'offset': offset, 'limit': limit}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching stations: {e}")
        return []
