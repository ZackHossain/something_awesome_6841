# THIS FILE IS ONLY FOR USE IN TESTING
import json
from api import api_post

tasks = [
    {"task_type":"ping"},
    {"task_type":"ping"}
]
# tasks = [
#     f'[{{"task_type":"{"pop"}"}}]',
#     f'[{{"task_type":"{"pop"}"}}]'
# ]

# results = [
#     {"content": "ENCRYPTED ALL FILES!", "success": True},
#     {"content": "Failed to encrypt files :(", "success": False}
# ]

targets = [
    {
        "ip": "127.0.0.1",
    }
]

def populate():
    # for result in results:
    # print("Sending:", results)
    # api_post('/results', results)
        
    for task in tasks:
        api_post('/tasks', task)
    
    for target in targets:
        api_post('/targets', target)

