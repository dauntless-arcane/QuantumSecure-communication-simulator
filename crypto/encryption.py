# crypto/encryption.py

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def derive_aes_key(bit_array):
    bit_string = ''.join(str(b) for b in bit_array)
    return hashlib.sha256(bit_string.encode()).digest()


def encrypt_message(message, quantum_key):
    aes_key = derive_aes_key(quantum_key)
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    return {
        "ciphertext": ciphertext,
        "iv": cipher.iv
    }


def decrypt_message(ciphertext, iv, quantum_key):
    aes_key = derive_aes_key(quantum_key)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext.decode()
