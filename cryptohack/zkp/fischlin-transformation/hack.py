from pwn import *
import json
from params import p, q, g
from hashlib import sha512
from Crypto.Util.number import bytes_to_long

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

# kinda a random oracle
def Totally_a_random_oracle(a0,a1,e,e0,e1,z0,z1):
    ROstep = sha512(b'my')
    ROstep.update(str(a0).encode())
    ROstep.update(b'very')
    ROstep.update(str(a1).encode())
    ROstep.update(b'cool')
    ROstep.update(str(e).encode())
    ROstep.update(b'random')
    ROstep.update(str(e0).encode())
    ROstep.update(b'oracle')
    ROstep.update(str(e1).encode())
    ROstep.update(b'for')
    ROstep.update(str(z0).encode())
    ROstep.update(b'fischlin')
    ROstep.update(str(z1).encode())
    res = bytes_to_long(ROstep.digest())
    return res




conn = remote('archive.cryptohack.org', 3583)

attempts = 2**4

for round in range(64):
    msg = conn.recvline()
    print(msg)
    msg = conn.recvline()
    print(msg)

    got = False

    for i in range(attempts):
        print('Round', round, 'attemp', i)

        y0 = int(conn.recvline().strip().split()[-1].decode())
        y1 = int(conn.recvline().strip().split()[-1].decode())

        msg = conn.recvuntil(b'which witness do you want to see?')
        print(msg)
        conn.sendline(b'0')

        w0 = int(conn.recvline().strip().split()[-1].decode())

        msg = conn.recvline()
        print(msg)

        proof = recvjson(conn)
        a0 = proof["a0"]
        a1 = proof["a1"]
        e  = proof["e"]
        e0 = proof["e0"]
        e1 = proof["e1"]
        z0 = proof["z0"]
        z1 = proof["z1"]


        # Attack
        r0 = (z0 + (q - w0) * e0) % q

        t = 2**10
        B = 6

        # In each iteration, we will keep constant a1, e1, z1
        for e_ref in range(t):
            eb = e_ref ^ e1
            zb = (r0 + eb * w0) % q
    
            res = Totally_a_random_oracle(a0, a1, e_ref, eb, e1, zb, z1)
            if res < 2**(512-B):
                break
    
        print(e_ref, e)
        msg = conn.recvuntil(b'do you think you can guess my witness? (y,n)')
        if e_ref == e:
            conn.sendline(b'no')
            continue
        else:
            got = True
            conn.sendline(b'yes')
            msg = conn.recvuntil(b'which witness did the prover use?')
            conn.sendline(b'1')

        msg = conn.recvline()
        print(msg)
        msg = conn.recvline()
        print(msg)

        break

    if not got:
        msg = conn.recvuntil(b'which witness did the prover use?')
        conn.sendline(b'0')
        msg = conn.recvline()
        print(msg)
        msg = conn.recvline()
        print(msg)



msg = conn.recvline()
print(msg)
msg = conn.recvline()
print(msg)