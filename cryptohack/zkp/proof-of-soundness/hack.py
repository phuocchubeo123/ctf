from pwn import *
import os
import json
from Crypto.Util.number import bytes_to_long

def fast_pow(x, e, p):
    if e == 0:
        return 1
    y = fast_pow(x, e // 2, p)
    if e % 2 == 0:
        return (y * y) % p
    else:
        return (y * y * x) % p

conn = remote('socket.cryptohack.org', 13425)

u = conn.recvline()
print(u)


p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2
w = 0x5a0f15a6a725003c3f65238d5f8ae4641f6bf07ebf349705b7f1feda2c2b051475e33f6747f4c8dc13cd63b9dd9f0d0dd87e27307ef262ba68d21a238be00e83
y = 0x514c8f56336411e75d5fa8c5d30efccb825ada9f5bf3f6eb64b5045bacf6b8969690077c84bea95aab74c24131f900f83adf2bfe59b80c5a0d77e8a9601454e5

while True:
    # Generate random A
    r = os.urandom(512 // 8)
    r = bytes_to_long(r)
    r = r % q
    A = fast_pow(g, r, p)
    if fast_pow(A, q, p) != 1:
        continue
    print(r)
    data = {
        "a": A
    }
    data_json = json.dumps(data)

    print(data_json)
    
    conn.sendline(data_json.encode())
    break


msg = json.loads(conn.recvline().decode())
print(msg)

e = int(msg["e"])
print(r)
z = (r + e * w) % q

print((fast_pow(y, e, p) * A) % p)
print(fast_pow(g, z, p))

data = {
    "z": z
}
data_json = json.dumps(data)
print(data_json)
conn.sendline(data_json.encode())

msg = json.loads(conn.recvline().decode())
print(msg)