from mycipher import MyCipher
import hashlib
import datetime
import random
from tqdm import tqdm

isLogged = False
username = ''
d = {}

def make_token(data1: str, data2: str):
    sha256 = hashlib.sha256()
    sha256.update(data1.encode())
    right = sha256.hexdigest()[:20]
    sha256.update(data2.encode())
    left = sha256.hexdigest()[:12]
    token = left + right
    return token

def main():
    for minutes in tqdm(range(60)):
        for sec in range(60):
            for randnum in range(10):
                Register(minutes, sec, randnum)
                Decrypt(bytes.fromhex('061ff06da6fbf8efcd2ca0c1d3b236aede3f5d4b6e8ea24179'));

def Register(minutes, sec, randnum):  # Register user into the system, not sure if helpful
    global d
    global username
    username = 'gureisya'
    data1 = f'user: {username}, {minutes}:{sec}'
    data2 = f'{username}'+str(randnum)
    d[username] = make_token(data1, data2)
    # print('Registered successfully!')
    # print('Your token is:', d[username])
    return

def Decrypt(plaintext):
    global d
    global username
    token = d[username]
    sha256 = hashlib.sha256()
    sha256.update(token.encode())
    key = sha256.hexdigest()[:32]
    nonce = token[:12]
    cipher = MyCipher(key.encode(), nonce.encode())
    ciphertext = cipher.encrypt(plaintext)
    # print('username:', username)
    try:
        decoded = ciphertext.decode()
        print(decoded)
    except UnicodeDecodeError:
        pass
    return

if __name__ == '__main__':
    main()