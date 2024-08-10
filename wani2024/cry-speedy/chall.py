from cipher import MyCipher, rotl
from Crypto.Util.number import *
from Crypto.Util.Padding import *
import os
from tqdm import tqdm

ct = b'"G:F\xfe\x8f\xb0<O\xc0\x91\xc8\xa6\x96\xc5\xf7N\xc7n\xaf8\x1c,\xcb\xebY<z\xd7\xd8\xc0-\x08\x8d\xe9\x9e\xd8\xa51\xa8\xfbp\x8f\xd4\x13\xf5m\x8f\x02\xa3\xa9\x9e\xb7\xbb\xaf\xbd\xb9\xdf&Y3\xf3\x80\xb8'

mod = 0xFFFFFFFFFFFFFFFF
s0 = bytes_to_long(ct[:8])
encrypted_first_block = ct[8:16]

print(mod)
print(s0)

for c1 in tqdm(range(119, 128)):
    for c2 in range(128):
        for c3 in range(128):
            secret = b'FLAG{' + long_to_bytes(c1) + long_to_bytes(c2) + long_to_bytes(c3)
            key = [secret[i] ^ encrypted_first_block[i] for i in range(8)]
            # print('key:', key)
            tot = 0
            for i in range(8):
                tot += key[i] << (i * 8);

            s1 = (tot + mod - s0 + 1) & mod

            new_tot = (s1 + s0) & mod
            new_key = []
            for _ in range(8):
                new_key.append(new_tot & 0xFF)
                new_tot >>= 8
            # print(new_key)
            # print('s1:', s1)


            cipher = MyCipher(s0, s1)

            s1 ^= s0
            X = (rotl(s0, 24) ^ s1 ^ (s1 << 16)) & mod

            if X == bytes_to_long(ct[16:24]):
                print('FOUND!')
                pt = cipher.decrypt(ct)
                print(pt)
                print([i for i in pt])
                break
