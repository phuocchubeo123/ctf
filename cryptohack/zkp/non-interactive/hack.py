from pwn import *
import os
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from hashlib import sha512

def recvjson(conn):
    return json.loads(conn.recvline().decode())

def sendjson(data, conn):
    conn.sendline(json.dumps(data).encode())

def fast_pow(x, e, p):
    if e == 0:
        return 1
    y = fast_pow(x, e // 2, p)
    if e % 2 == 0:
        return (y * y) % p
    else:
        return (y * y * x) % p

# Diffie-Hellman group (512 bits)
# p = 2*q + 1 where p,q are both prime, and 2 modulo p generates a group of order q
p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2
w = 0xdb968f9220c879b58b71c0b70d54ef73d31b1627868921dfc25f68b0b9495628b5a0ea35a80d6fd4f2f0e452116e125dc5e44508b1aaec89891dddf9a677ddc0


conn = remote('socket.cryptohack.org', 13428)

msg = conn.recvline()
print(msg)

msg = recvjson(conn)
print(msg)
y = msg["y"]

while True:
    # Generate random A
    r = os.urandom(512 // 8)
    r = bytes_to_long(r)
    r = r % q
    A = fast_pow(g, r, p)
    if fast_pow(A, q, p) != 1:
        continue
    print(r, A)
    break

fiat_shamir_input = str(A).encode()
e = bytes_to_long(sha512(fiat_shamir_input).digest()) % (2 ** 511)

z = (r + e * w) % q

data = {"a": A, "z": z}

sendjson(data, conn)

msg = recvjson(conn)
print(msg)