from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256, Public_key, Private_key

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

a = 6364136223846793005
print(bin(a))
print(len(bin(a)[2:]))
print(a % 94)
print(bin(a-1))

m = 2 ** 64
print('Analyse m')
print(m % 94)

tot = 0

print("The sequence analysis")
for i in range(200):
    tot = pow(a, i, m)
    tot %= m
    print(i, tot, tot % 94)