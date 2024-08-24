from hamiltonicity import pedersen_commit, pedersen_open
from hamiltonicity import commit_to_graph, open_graph, permute_graph
from hamiltonicity import hash_committed_graph, testcycle
from hamiltonicity import comm_params, get_r_vals
from hamiltonicity import P, q, h1, h2
from Crypto.Util.number import inverse
import json
import random
from pwn import * 

numrounds = 128


# Graph with no hamiltonian cycle
# Break the fiat shamir to convince the server this has a cycle to get the flag :)
N = 5
G = [
    [0,0,1,0,0],
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,0,0,0,1],
    [0,0,0,1,0]
]

many_G = []
for i in range(100):
    initial_graph = [[random.randint(0, 1) for j in range(N)] for k in range(N)]
    for j in range(N):
        initial_graph[j][(j + 1) % N] = 1
    many_G.append(initial_graph)


conn = remote('archive.cryptohack.org', 34597)

FS_state = b''

A_vals = []
z_vals = []

comm = (((h2 ** 2) % P - h1) * inverse((10 ** 312) % P, P)) % P * (10 ** 312) + h1
b1 = int(str(comm) + str(comm)[:-len(str(h1))])
b2 = h1

u = (h1 * (h2 ** 2)) % P

print(comm % P == (h2 ** 2) % P)
assert pedersen_open(comm, 0, 2)
print('done')

assert pedersen_open(u, 1, 2)
print('done')

print(comm)
print(b1)
print(b2)
print(str(b1) + str(b2) == str(comm) + str(comm))

for i in range(numrounds):
    openings = [[[0, 2] for j in range(N)] for k in range(N)]
    A = [[0 for j in range(N)] for k in range(N)]
    for j in range(N):
        for k in range(N):
            if G[j][k] == 1:
                A[j][k] = (h1 * (h2 ** 2)) % P
            else:
                A[j][k] = comm
            openings[j][k][0] = G[j][k]

    A_vals.append(A)
    z_vals.append([[i for i in range(N)], openings])


for i in range(numrounds):
    FS_state = hash_committed_graph(A_vals[i], FS_state, comm_params)

challenge_bits = bin(int.from_bytes(FS_state, 'big'))[-numrounds:]

print(challenge_bits)

for i in range(numrounds):
    if challenge_bits[i] == '1':
        A = A_vals[i]
        openings = z_vals[i][1]
        A[2][3] = b1
        A[2][4] = b2
        openings[2][4][1] = 0
        A[3][0] = b1
        A[3][1] = b2
        openings[3][1][1] = 0

        A_vals[i] = A
        cycle = [[1, 0], [0, 2], [2, 4], [4, 3], [3, 1]]
        z_vals[i][0] = cycle
        z_vals[i][1] = [openings[j][k][1] for j, k in cycle]

        print(i, z_vals[i][0], z_vals[i][1])

msg = conn.recvline()
print(msg)

for i in range(numrounds):
    print('Send round', i)
    msg = conn.recvuntil(b'send fiat shamir proof: ')
    print(msg)
    data = {"A": A_vals[i], "z": z_vals[i]}
    conn.sendline(json.dumps(data).encode())

msg = conn.recvline()
print(msg)

for i in range(numrounds):
    msg = conn.recvline()
    print(msg)
    msg = conn.recvline()
    print(msg)
    msg = conn.recvline()
    print(msg)

msg = conn.recvline()
print(msg)
msg = conn.recvline()
print(msg)