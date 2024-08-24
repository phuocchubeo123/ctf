from pwn import *
import random
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm

def gen(n):
    p, i = [0] * n, 0
    for j in random.sample(range(1, n), n - 1):
        p[i], i = j, j
    return tuple(p)


def gexp(g, e):
    res = tuple(g)
    while e:
        if e & 1:
            res = tuple(res[i] for i in g)
        e >>= 1
        g = tuple(g[i] for i in g)
    return res


def enc(k, m, G):
    if not G:
        return m
    mod = len(G[0])
    return gexp(G[0], k % mod)[m % mod] + enc(k // mod, m // mod, G[1:]) * mod


def inverse(perm):
    res = list(perm)
    for i, v in enumerate(perm):
        res[v] = i
    return res

def nxt(curr, g):
    return tuple(curr[i] for i in g)

conn = remote('sometrick.chals.sekai.team', 1337, ssl = True)

msg = conn.recvline()
print(msg)
CIPHER_SUITE = int((msg.strip().split()[-1]).decode().split('.')[-1])

print(CIPHER_SUITE)


random.seed(CIPHER_SUITE)

GSIZE = 8209
GNUM = 79
mod = GSIZE

LIM = GSIZE**GNUM

G = [gen(GSIZE) for i in range(GNUM)]

msg = conn.recvline()
print(msg)
bob_encr = int(msg.strip().split()[-1].decode())
print(bob_encr)

msg = conn.recvline()
print(msg)
alice_encr = int(msg.strip().split()[-1].decode())
print(alice_encr)

msg = conn.recvline()
print(msg)
bob_decr = int(msg.strip().split()[-1].decode())
print(bob_decr)

# Crack alice_key from alice_encr and bob_encr
k = int(bob_encr)
res = int(alice_encr)
alice_key = 0
for i in tqdm(range(GNUM)):
    curr = gexp(G[i], k % GSIZE)
    for alice in range(GSIZE):
        if curr[alice] == res % GSIZE:
            break
    alice_key += alice * (GSIZE ** i)
    k //= GSIZE
    res //= GSIZE

print('Found alice_key', alice_key)
print(enc(bob_encr, alice_key, G) == alice_encr)

# Crack bob_key from bob_decr and alice_encr
k = int(alice_encr)
res = int(bob_decr)
bob_key = 0
for i in tqdm(range(GNUM)):
    curr = gexp(inverse(G[i]), k % GSIZE)
    for bob in range(GSIZE):
        if curr[bob] == res % GSIZE:
            break
    bob_key += bob * (GSIZE ** i)
    k //= GSIZE
    res //= GSIZE

print('Found bob_key', bob_key)
print(enc(alice_encr, bob_key, [inverse(i) for i in G]) == bob_decr)


# Crack FLAG from bob_encr and bob_key 
m = int(bob_key)
res = int(bob_encr)
FLAG = 0
for i in tqdm(range(GNUM)):
    curr = G[i]
    for k in range(GSIZE):
        if curr[m % GSIZE] == res % GSIZE:
            break
        curr = nxt(curr, G[i])
    FLAG += k * (GSIZE ** i)
    m //= GSIZE
    res //= GSIZE

print('Found flag', FLAG)
print(enc(FLAG, bob_key, G) == bob_encr)
print(long_to_bytes(FLAG))