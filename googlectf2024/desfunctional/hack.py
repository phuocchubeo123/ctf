from pwn import *
# from Crypto.Cipher import DES3

conn = remote('desfunctional.2024.ctfcompetition.com', 1337)

# Read the options
for i in range(5):
    u = conn.recvline()
    print(u)

conn.send(b'1\n')

challenge = conn.recvline()
print('The challenge is:')
print(challenge)
print(len(challenge))
print(challenge[:-1] + challenge[:-1])

decrypteds = []

for i in range(50):
    print('New iteration')
    for j in range(4):
        u = conn.recvline()
        print(u)

    conn.send(b'2\n')

    lmao = conn.recvuntil(b'(hex) ct: ')
    print(lmao)
    
    conn.send(challenge[:-1] * 3 + b'\n')

    decrypted = conn.recvline()
    print('Decrypted of challenge in this round is:')
    for i in range(0, len(decrypted), 64):
        print(decrypted[i:i+64])
    print()
    
    if decrypted in decrypteds:
        # The last one is the plain challenge
        print('Found plain challenge')
        for j in range(4):
            u = conn.recvline()
            print(u)

        conn.send(b'3\n')

        lmao = conn.recvuntil(b'(hex) pt: ')
        print(lmao)

        print('The attempted hex for challenge is:')
        print(decrypted)
        conn.send(decrypted)

        lmao = conn.recvline()
        print(lmao)

        break
    

    decrypteds.append(decrypted)