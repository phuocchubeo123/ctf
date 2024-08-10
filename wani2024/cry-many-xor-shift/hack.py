from tqdm import tqdm

N = 7
M = 17005450388330379
WORD_SIZE = 32
WORD_MASK = (1 << WORD_SIZE) - 1

state = [1, 0, 0, 0, 0, 0, 0]

def xor_shift():
    global state
    t = state[0] ^ ((state[0] << 11) & WORD_MASK)
    for i in range(N-1):
        state[i] = state[i+1]  # shift all states to the left
    state[-1] = (state[-1] ^ (state[-1] >> 19)) ^ (t ^ (t >> 8)) # 

def all_num(state):
    u = state[0] ^ (state[-1] << 32)
    return u

all_state_dict = dict()
all_state_dict[all_num(state)] = 1
for i in tqdm(range(100000000)):
    xor_shift()

    current_num = all_num(state)
    # print(current_num)
    # print(state)
    if i >= 100 and current_num in all_state_dict:
        print('FOUND LOOP')
        print(i)
        break

    all_state_dict[current_num] = 1
