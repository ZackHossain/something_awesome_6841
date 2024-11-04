import requests
import json

from config import listener_host

def api_get(endpoint):
    response_raw = requests.get(listener_host + endpoint)
    
    print(response_raw.status_code)
    if response_raw.status_code == 204:
        return []
    
    response_json = json.loads(response_raw.text)
    return response_json

def api_post(endpoint, payload):
    print(payload)
    response_raw = requests.post(listener_host + endpoint, json=payload)
    print(response_raw.status_code)
    if response_raw.status_code == 204 or response_raw.status_code == 500:
        return []
    
    response_json = json.loads(response_raw.text)
    print(response_json)
    return response_json

def api_put(endpoint, payload):
    response_raw = requests.put(listener_host + endpoint, json=payload)
    response_json = json.loads(response_raw.text)
    return response_json