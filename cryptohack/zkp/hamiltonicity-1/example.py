from hamiltonicity import pedersen_commit, pedersen_open
from hamiltonicity import commit_to_graph, open_graph, permute_graph
from hamiltonicity import hash_committed_graph, testcycle
from hamiltonicity import comm_params, get_r_vals
import json
import random
from pwn import process


numrounds = 128
LocalTest = True

# Graph with Hamiltonian cycle (0,4) (4,2) (2,3) (3,1) (1,0)
# You can use this locally to test correct proofs :)
N = 5
cycle = [(0,4), (4,2), (2,3), (3,1), (1,0)]
G = [
    [0,1,1,0,1],
    [1,0,0,0,0],
    [0,0,0,1,0],
    [0,1,1,0,0],
    [1,0,1,1,0]
]   


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



# example running locally. 
# Set LocalTest = True in the challenge file, then this should solve it for localflag ^^
with process(["python3 chal.py"], shell=True) as rem:
    rem.recvuntil(b'prove to me that G has a hamiltonian cycle!')
    FS_state = b''

    for i in range(numrounds):
        print(f"starting round {i}")
        A_permuted, openings, permutation = gen_A(G,N)
        FS_state = hash_committed_graph(A_permuted, FS_state, comm_params)
        # take one bit of hash as challenge
        challenge = FS_state[-1] & 1

        if challenge:
            print("challenge bit is 1")
            # permute the hamiltonian cycle indexes to open
            permuted_cycle = []
            for x in cycle:
                permuted_cycle.append([permutation.index(x[0]), permutation.index(x[1])] )
            
            # get the ordered list of r values to open the commitments to 1 with
            openings = get_r_vals(openings, N, cycle)
            z = [permuted_cycle, openings]
            rem.recvuntil(b"send fiat shamir proof: ")
            rem.sendline(json.dumps({"A" : A_permuted, "z": z}))
            resp = rem.readline()
            print(resp)

        else:
            print("challenge bit is 0")
            # permute openings
            openings = permute_graph(openings,N,permutation)
            z = [permutation, openings]
            rem.recvuntil(b"send fiat shamir proof: ")
            rem.sendline(json.dumps({"A" : A_permuted, "z": z}))
            resp = rem.readline()
            print(resp)
    rem.interactive()
