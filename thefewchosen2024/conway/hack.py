import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

with open('output.txt', 'r') as f:
    initial = f.readline().strip()
    ctx = f.readline().strip()

curr = ''
cnt = 0
new_initial = ''
for c in initial:
    if c == curr:
        cnt += 1
        continue

    if curr == '':
        curr = c
        cnt = 1
        continue

    new_initial += str(cnt)
    new_initial += curr
    curr = c
    cnt = 1

new_initial += str(cnt)
new_initial += curr

print(new_initial)
new_initial = int(new_initial)


h = hashlib.sha256()
h.update(str(new_initial).encode())
key = h.digest()

cipher = AES.new(key, AES.MODE_ECB)
ctx = bytes.fromhex(ctx)
print(ctx)

print(cipher.decrypt(ctx))


# TFCCTF{c0nway's_g4me_0f_sequences?}