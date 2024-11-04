import requests
import json
from config import listener_host


def api_get(endpoint):
    response_raw = requests.get(listener_host + endpoint).text
    
    # if the response does not contain a string, return an empty list
    if type(response_raw) is not str:
        return []
    response_json = json.loads(response_raw)
    return response_json

def api_post(endpoint, payload):
    response_raw = requests.post(listener_host + endpoint, json=payload)
    
    # if the response does not contain a string, return an empty list
    if type(response_raw) is not str:
        return []
    response_json = json.loads(response_raw)
    return response_json