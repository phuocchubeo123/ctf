from pwn import *
import os
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from hashlib import sha512

def recvjson(conn):
    return json.loads(conn.recvline().decode())

def sendjson(data, conn):
    conn.sendline(json.dumps(data).encode())

def sendint(x, conn):
    conn.sendline(str(x).encode())

def fast_pow(x, e, p):
    if e == 0:
        return 1
    y = fast_pow(x, e // 2, p)
    if e % 2 == 0:
        return (y * y) % p
    else:
        return (y * y * x) % p

from params_4a7ef8baab87dce725db18a42fc9c862 import p, q, g
w0 = 0x5a0f15a6a725003c3f65238d5f8ae4641f6bf07ebf349705b7f1feda2c2b051475e33f6747f4c8dc13cd63b9dd9f0d0dd87e27307ef262ba68d21a238be00e83
y0 = 0x514c8f56336411e75d5fa8c5d30efccb825ada9f5bf3f6eb64b5045bacf6b8969690077c84bea95aab74c24131f900f83adf2bfe59b80c5a0d77e8a9601454e5
# w1 = REDACTED
y1 = 0x1ccda066cd9d99e0b3569699854db7c5cf8d0e0083c4af57d71bf520ea0386d67c4b8442476df42964e5ed627466db3da532f65a8ce8328ede1dd7b35b82ed617

conn = remote('archive.cryptohack.org', 11840)

## correctness

# sample random e1 and generate the corresponding proof (a_1, e_1, z_1)
e1 = bytes_to_long(os.urandom(512 // 8)) % q
z1 = bytes_to_long(os.urandom(512 // 8)) % q
a1 = fast_pow(g, z1, p) * inverse(fast_pow(y1, e1, p), p)

# generate a0 honestly
r0 = bytes_to_long(os.urandom(512 // 8)) % q
a0 = fast_pow(g, r0, p)

# input a0, a1
msg = conn.recvline()
print(msg)
msg = conn.recvline()
print(msg)

msg = conn.recvuntil(b'a0:')
print(msg)
sendint(a0, conn)
print(a0)

msg = conn.recvuntil(b'a1:')
print(msg)
sendint(a1, conn)
print(a1)

msg = conn.recvline()
print(msg)
s = int(msg.strip().split()[-1].decode())
print('s:', s)


# compute e0, z0
e0 = s ^ e1
z0 = r0 + e0 * w0

msg = conn.recvuntil(b'e0:')
print(msg)
sendint(e0, conn)
print(e0)

msg = conn.recvuntil(b'e1:')
print(msg)
sendint(e1, conn)
print(e1)

msg = conn.recvuntil(b'z0:')
print(msg)
sendint(z0, conn)
print(z0)

msg = conn.recvuntil(b'z1:')
print(msg)
sendint(z1, conn)
print(z1)


## Special Soundness
for i in range(4):
    msg = conn.recvline()
    print(msg)

# Transcript 1
msg = conn.recvline()
print(msg)

data = []
for i in range(7):
    msg = conn.recvline()
    data.append(int(msg.strip().split()[-1].decode()))

a0, a1, s, e0, e1, z0, z1 = data

# Transcript 2
msg = conn.recvline()
print(msg)

data = []
for i in range(7):
    msg = conn.recvline()
    data.append(int(msg.strip().split()[-1].decode()))

a0, a1, s2, e02, e12, z02, z12 = data