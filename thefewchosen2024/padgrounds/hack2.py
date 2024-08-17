from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import base64
import random
from collections import Counter
from tqdm import tqdm
import pwn

def byte_xor(x1, x2):
    return bytes([b1^b2 for b1, b2 in zip(x1, x2)])

chars = list('_bdefgmnprsu012345')

conn = pwn.remote('challs.tfcctf.com', 32277)

u = conn.recvline()

sth = os.urandom(16)

iv_and_ct = u.decode().strip().split()[-1]
iv_and_ct = base64.b64decode(iv_and_ct)
iv = iv_and_ct[:16]
ct = iv_and_ct[16:]
print(iv)
print(ct)
print(len(iv), len(ct))

u = conn.recvline()
print(u)

prev_chunk = ct[-48:-32]

# test_iv = b'0' * 15 + chr(ord('}') ^ 1).encode()
# test_ct = ct[-16:]
# test_iv = byte_xor(test_iv, prev_chunk)

# print(test_iv, test_ct)

# cnt = 0

# for i in tqdm(range(50)):
#     send_ct = test_iv + test_ct
#     send_ct = base64.b64encode(send_ct)
#     # print(send_ct)
#     conn.sendline(send_ct)
#     u = conn.recvline()
#     u = u.strip().decode()
#     if u == 'False':
#         cnt += 1

# print('The number of False when XORing with } is', cnt)

revealed = '1ngs_m4_fr1end5_'


for k in range(16):
    found = False
    for j in range(len(chars)):
        curr = chars[j]
        l = len(revealed)
        test_iv = b't' * (16 - l - 1) + byte_xor((curr + revealed).encode(), chr(l+1).encode() * (l+1))
        test_iv = byte_xor(test_iv, prev_chunk)
        test_ct = ct[-32:-16]
        send_ct = test_iv + test_ct
        send_ct = base64.b64encode(send_ct)

        print(test_iv, test_ct)
        print(send_ct)
        print(base64.b64decode(send_ct))

        cnt = 0

        for i in tqdm(range(50)):
            # print(send_ct)
            conn.sendline(send_ct)
            u = conn.recvline()
            u = u.strip().decode()
            if u == 'False':
                cnt += 1

        if cnt < 30:
            print('FOUND ANOTHER CHARACTER!', curr)
            revealed = curr + revealed
            print('Revealed:', revealed)
            found = True
            break

    if not found:
        print('Reached CTF!')
        break