from hamiltonicity import pedersen_commit, pedersen_open
from hamiltonicity import commit_to_graph, open_graph, permute_graph
from hamiltonicity import hash_committed_graph, testcycle
from hamiltonicity import comm_params, get_r_vals
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


def gen_A(G,N):
    # commit to graph
    A, openings = commit_to_graph(G, N)
    # shuffle graph
    permutation = [i for i in range(N)]
    random.shuffle(permutation)
    A_permuted = permute_graph(A,N,permutation)

    assert G == open_graph(A,N,openings)
    assert permute_graph(G,N,permutation) == open_graph(A_permuted,N, permute_graph(openings,N,permutation))
    
    return A_permuted, openings, permutation


conn = remote('archive.cryptohack.org', 14635)

msg = conn.recvuntil(b'prove to me that G has a hamiltonian cycle!')
print(msg)
FS_state = b''

for i in range(numrounds):
    print('Round number:', i)
    while True:
        A_permuted, openings, permutation = gen_A(G,N)
        fake_FS_state = hash_committed_graph(A_permuted, FS_state, comm_params)
        if fake_FS_state[-1] & 1:
            continue
        FS_state = fake_FS_state
        break


    print("challenge bit is 0")
    # permute openings
    openings = permute_graph(openings,N,permutation)
    z = [permutation, openings]
    conn.recvuntil(b"send fiat shamir proof: ")
    conn.sendline(json.dumps({"A" : A_permuted, "z": z}))
    resp = conn.readline()
    print(resp)

msg = conn.recvline()
print(msg)
msg = conn.recvline()
print(msg)