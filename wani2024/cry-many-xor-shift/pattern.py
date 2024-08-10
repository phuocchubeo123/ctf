from tqdm import tqdm

WORD_SIZE = 32
WORD_MASK = (1 << WORD_SIZE) - 1

pos = (1<<5)
all_pos = [pos]
all_pos_dict = dict()
all_pos_dict[pos] = 1
for i in tqdm(range(100000)):
    pos = pos ^ ((pos << 11) & WORD_MASK)
    pos = pos ^ (pos >> 8)
    
    all_pos.append(pos)

    if i > 3 and (pos in all_pos_dict):
        start_loop = 0
        for _ in range(len(all_pos)):
            if all_pos[_] == pos:
                start_loop = _
                break
        print('FOUND LOOP', pos)
        print(i*7, start_loop, i*7-start_loop)
        print(i*7)
        exit()
    
    for j in range(6):
        pos = pos ^ ((pos >> 19))
        all_pos.append(pos)
        if i > 3 and (pos in all_pos_dict):
            start_loop = 0
            for _ in range(len(all_pos)):
                if all_pos[_] == pos:
                    start_loop = _
                    break
            print('FOUND LOOP', pos)
            print(i*7+j+1, start_loop, i*7+j+1-start_loop)
            print(i*7+j+1)
            exit()

    for p in all_pos[-7:]:
        all_pos_dict[p] = 1

