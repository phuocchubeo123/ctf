import os
from secrets import randbits
from Crypto.Util.number import bytes_to_long


FLAG = b"FLAG{" + b"*" * 510 + b"}"
m = bytes_to_long(FLAG)
assert m.bit_length() >= 512


def encrypt(m: int, n: int = 512) -> int:
    x = 0
    for i in range(n):
        x <<= 1
        x += m * randbits(1)
        if i >= n // 2:
            x ^= randbits(1)
    return x



X = [encrypt(m) for _ in range(4)]
# print(X)

for i in range(5):
    print(randbits(1))