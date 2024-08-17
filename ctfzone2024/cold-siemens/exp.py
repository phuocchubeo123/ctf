from gmpy2 import iroot
import math

x = 15
prec = 20

y = iroot(x * (10 ** (prec * 4)), 4)[0] % (10 ** prec)

print(y)
print()

print(y ** 4)
print(4 * y**3)
print(6 * y**2)
print(4 * y)
print(10 ** (prec * 4))


u = 1.96798967126543041853

for i in range(100):
    v = math.floor(u)
    u = 1 / (u - v)
    print(v, u)

print(math.log(10) / math.log(16) * 666)