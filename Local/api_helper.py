import requests
import os

def get_stations(offset=0, limit=0, search=""):
    import requests

    url = f"http://localhost:5001/stations"
    params = {
        'offset': offset,
        'limit': limit,
        'search': search
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching stations: {e}")
        return []
