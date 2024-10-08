from Crypto.Util.number import *
from Crypto.Util.Padding import *

def rotl(x, y):
    x &= 0xFFFFFFFFFFFFFFFF
    return ((x << y) | (x >> (64 - y))) & 0xFFFFFFFFFFFFFFFF

class MyCipher:
    def __init__(self, s0, s1):
        self.X = s0
        self.Y = s1
        self.mod = 0xFFFFFFFFFFFFFFFF
        self.BLOCK_SIZE = 8
    
    def get_key_stream(self):
        print('X:', self.X)
        s0 = self.X
        s1 = self.Y
        sum = (s0 + s1) & self.mod
        s1 ^= s0

        # print(s0, s1)

        key = []
        for _ in range(8):
            key.append(sum & 0xFF)
            sum >>= 8

        # print('this key:', key)

        self.X = (rotl(s0, 24) ^ s1 ^ (s1 << 16)) & self.mod
        self.Y = rotl(s1, 37) & self.mod
        return key
    
    def encrypt(self, pt: bytes):
        ct = b''
        for i in range(0, len(pt), self.BLOCK_SIZE):
            ct += long_to_bytes(self.X)
            key = self.get_key_stream()
            block = pt[i:i+self.BLOCK_SIZE]
            ct += bytes([block[j] ^ key[j] for j in range(len(block))])
        return ct

    def decrypt(self, ct: bytes):
        pt = b''
        for i in range(0, len(ct), 2 * self.BLOCK_SIZE):
            key = self.get_key_stream()
            print(bytes_to_long(ct[i:i+self.BLOCK_SIZE]))
            block = ct[i+self.BLOCK_SIZE:i+2*self.BLOCK_SIZE]
            pt += bytes([block[j] ^ key[j] for j in range(len(block))])
        return pt