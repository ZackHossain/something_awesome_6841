import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from result import result

def decrypt(task, info):
    # get the symmetric key from server
    c_sym = ''
    files = []
    for file in os.listdir():
        if file.endswith('_enc'):
            files.append(file)
    
    cipher = Cipher(algorithms.AES(c_sym), mode=algorithms.AES.MODE_GCM())
    decryptor = cipher.decryptor()
    for file in files:
        with open(file, 'rb') as fd:
            ciphertext = fd.read()
            tag = ciphertext[-16:]
            ciphertext = ciphertext[:-16]
            
            plaintext = decryptor.update(ciphertext) + decryptor.finalize_with_tag(tag)
        with open(file, 'wb') as fd:
            fd.write(plaintext)
    
    return result(task['id'], task['task_id'], True, f'ALL FILES DECRYPTED')