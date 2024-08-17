from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64
import random
from collections import Counter
from tqdm import tqdm

def byte_xor(x1, x2):
    return bytes([b1^b2 for b1, b2 in zip(x1, x2)])

u = b'a' * 15
u = pad(u, 16)
print(u)

for i in range(1, 17):
    print(chr(i).encode(), chr(i^1).encode())

key = os.urandom(16)
iv = os.urandom(16)

FLAG = b'CTF{pdz}' + chr(8).encode() * 8

cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(FLAG)

for i in range(1, 17):
    iv2 = chr(0).encode() * 15 + chr(i^1).encode()
    iv2 = byte_xor(iv, iv2)
    cipher2 = AES.new(key, AES.MODE_CBC, iv2)
    pt = cipher2.decrypt(ct)
    print(pt)
    try:
        unpad(pt, 16)
        print('Can unpad', i)
    except:
        print('Cannot unpad', i)