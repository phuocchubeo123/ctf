from Crypto.Util.number import *

a, b = [88952575866827947965983024351948428571644045481852955585307229868427303211803239917835211249629755846575548754617810635567272526061976590304647326424871380247801316189016325247, 67077340815509559968966395605991498895734870241569147039932716484176494534953008553337442440573747593113271897771706973941604973691227887232994456813209749283078720189994152242]
p = 396430433566694153228963024068183195900644000015629930982017434859080008533624204265038366113052353086248115602503012179807206251960510130759852727353283868788493357310003786807

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist for a = {a} and m = {m}")
    return x % m

def fast_pow(a, e, m):
    if e == 0:
        return 1
    b = fast_pow(a, e // 2, m)
    if e % 2 == 0:
        return (b * b) % m
    else:
        return ((b * b) * a) % m

# Find 13^m and 37^m
# b = 13^m + 37^m
# a = 13^{m-1} + 37^{m-1}
# 37a - b = 13^{m-1} (37 - 13)
# (37a - b) / 24 * 13 = 13^m

c = ((a * 37 - b) * mod_inverse(24, p) * 13) % p
print(c)


# It is really likely that p is a smooth prime
u = p-1
prime_factor = []

for i in range(2, 10000000):
    while u % i == 0:
        u //= i
        prime_factor.append(i)

print(prime_factor)
print('Unique?', len(set(prime_factor)) == len(prime_factor))

crt = []

for q in prime_factor:
    print('Find CRT mod', q)
    x = fast_pow(13, (p-1) // q, p)
    y = fast_pow(c, (p-1) // q, p)
    print('base:', x)
    print('target:', y)
    
    curr = 1
    for i in range(q):
        if curr == y:
            crt.append(i)
            break
        curr = (curr * x) % p

print(crt)

tot = 0
for i in range(len(crt)):
    r = crt[i]
    q = prime_factor[i]
    component = (p - 1) // q
    tot += component * mod_inverse(component, q) * r

tot = tot % (p-1)
print(tot)

print('Check if power is correct:')
print(fast_pow(13, tot, p))
print(c)

# The power is correct, now extract flag

for i in range(100):
    curr = (p-1) * i + tot
    print(long_to_bytes(curr))