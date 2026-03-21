from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

key = get_random_bytes(32)


def encrypt(plain_text, key):

    cipher_encrypt = AES.new(key, AES.MODE_CBC)
    padded = pad(plain_text.encode("utf-8"), AES.block_size)
    encrypt = cipher_encrypt.encrypt(padded)
    encoded = b64encode(encrypt)

    return encoded, cipher_encrypt.iv


def decrypt(encoded, iv):

    cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)
    decoded = b64decode(encoded)
    decrypt = cipher_decrypt.decrypt(decoded)
    unpadded = unpad(decrypt, AES.block_size).decode("utf-8")

    return unpadded


encoded, iv = encrypt("twilight is the best movie ever", key)
print(encoded, iv)
print(decrypt(encoded, iv))
