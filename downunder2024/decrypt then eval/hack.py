from pwn import *

conn = remote('2024.ductf.dev', 30020)

u = conn.recvuntil(b'ct: ')
print(u)


for num in range(2 ** 8):
    if num % 1000 == 0:
        print('Step:', num)

    num_hex = hex(num)[2:]
    num_bytes = num_hex.encode()
    if len(num_bytes) % 2 == 1:
        num_bytes = num_bytes + b'0'

    conn.send(num_bytes + b'\n')
    u = conn.recvline()

    if u != b'invalid ct!\n':
        print(num_bytes, u)
        # break
    
    u = conn.recvuntil(b'ct: ')