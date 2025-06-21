import os
import requests
from flask import request

def get_iot_data(iot_id):
    base_url = os.getenv('IOT_API_URL')
    if iot_id == 1:
        urls = [
            base_url+"/weather/values",
            base_url+"/weather/position",
            base_url+"/stream1/jpg"
        ]
    elif iot_id == 2:
        urls = [
            base_url+"/socket/values",
            base_url+"/socket/position",
            base_url+"/stream2/jpg"
        ]
    else:
        return {"error": "Invalid iot_id"}, 400

    results = {}
    for url in urls:
        try:
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code == 200:
                if url.endswith('/jpg'):
                    # Em vez de enviar a imagem, envia o link para o endpoint local que irá expor a imagem
                    results['image_url'] = url
                elif url.endswith('/values'):
                    results['values'] = response.json()
                elif url.endswith('/position'):
                    results['position'] = response.json()
            else:
                return {"error": f"Failed to fetch {url}"}, response.status_code
        except Exception as e:
            return {"error": str(e)}, 500

    return results, 200
