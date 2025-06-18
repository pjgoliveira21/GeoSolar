import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Garante que as variáveis do .env são carregadas, se usares ficheiro .env

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
        print(f"[get_stations] Erro ao buscar estações: {e}")
        return []