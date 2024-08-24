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

def nxt(curr, g):
    return tuple(curr[i] for i in g)

GSIZE = 8209
GNUM = 79
mod = GSIZE

LIM = GSIZE**GNUM

G = [gen(GSIZE) for i in range(GNUM)]

for i in range(10):
    u = gexp(G[0], i)
    curr = tuple(G[0])
    for j in range(20):
        if curr == u:
            print('First for', i, 'is', j)
            break
        curr = nxt(curr, G[0])