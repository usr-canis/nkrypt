#!/usr/bin/env python3

import argparse
import os
from getpass import getpass
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def derive_key(password):

    salt = b'\x87\xd9\xf8A\x1e\xf6F\xeb\x98\xdf-\xa4\xdb6\xc6'  
   
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path, encryption_key):
   
    with open(file_path, 'rb') as f:
        data = f.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(16) 
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as f:
        f.write(iv + encrypted_data)

    print("File encrypted successfully.")

def decrypt_file(file_path, encryption_key):
    with open(file_path, 'rb') as f:
        data = f.read()

    iv = data[:16]
    encrypted_data = data[16:]

    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    with open(file_path, 'wb') as f:
        f.write(unpadded_data)

    print("File decrypted successfully.")

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt files using Nkrypt')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform: encrypt or decrypt')
    parser.add_argument('filepath', help='File path')
    args = parser.parse_args()

    password = getpass("Enter password: ")
    encryption_key = derive_key(password)

    if args.action == 'encrypt':
        encrypt_file(args.filepath, encryption_key)
    elif args.action == 'decrypt':
        decrypt_file(args.filepath, encryption_key)

if __name__ == '__main__':
    main()

