from pwn import *
import os
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

def recvjson(conn):
    return json.loads(conn.recvline().decode())

def sendjson(data, conn):
    conn.sendline(json.dumps(data).encode())

p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2

conn = remote('socket.cryptohack.org', 13426)

msg = conn.recvline()
print(msg)

msg = recvjson(conn)
print(msg)
a = msg["a"]
y = msg["y"]

e = os.urandom(512 // 8)
e = bytes_to_long(e)
data = {"e": e}
sendjson(data, conn)

msg = recvjson(conn)
print(msg)
z = msg["z"]


msg = recvjson(conn)
print(msg)
a2 = msg["a2"]

e2 = os.urandom(512 // 8)
e2 = bytes_to_long(e2)
data = {"e": e2}
sendjson(data, conn)

msg = recvjson(conn)
print(msg)
z2 = msg["z2"]

flag = ((z2 - z) * inverse(e2 - e, q)) % q
print(long_to_bytes(flag))