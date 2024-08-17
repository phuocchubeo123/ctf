from pwn import *
import os
import random
from math import log

from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import iroot

conn = remote('cold_siemens.ctfz.zone', 1188)

flag = conn.recvline().strip().decode('utf-8').split()[-1]
flag = bytes.fromhex(flag)

print("The Encrypted flag is:", flag)
print("The flag length is:", len(flag))

u = conn.recvuntil(b'm: ')

for m_len in range(280, 281):
    print('Analysing with message length', m_len)
    message = b'\x00' * m_len
    conn.sendline(message.hex().encode())
    u = conn.recvline().strip().decode('utf-8').split()[-1]
    u = bytes.fromhex(u)
    print('The encrypted message is:', u)

    key = [x^y for x, y in zip(message, u)]
    key = bytes(key)
    print(key)
    for i in range(1, len(key)):
        j = min(i, len(key) - i)
        if key[:j] == key[i:i+j]:
            key = key[:i]
            break
    print(key)
    print(len(key))
    key = bytes_to_long(key)
    print(len(str(key)))