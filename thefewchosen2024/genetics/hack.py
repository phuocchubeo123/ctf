with open('genetics.txt', 'r') as f:
    ln = f.readline().strip().split()

translate = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

for dna in ln:
    tot = 0
    for c in dna:
        tot *= 4
        tot += translate[c]
    
    print(chr(tot), end = '')


# TFCCTF{1_w1ll_g3t_th1s_4s_4_t4tt00_V3ry_s00n}