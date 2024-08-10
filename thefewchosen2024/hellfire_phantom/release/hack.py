def fast_pow(x, ex, mod):
    if ex == 0:
        return 1
    y = fast_pow(x, ex//2, mod)
    if ex % 2 == 1:
        return y * y * x
    else:
        return y * y

p = 1154543773027194978300531105544404721440832315984713424625039
factor_phi = [2, 641, 900580166167858797426311314777226771794720995307888786759]
divisors = list(factor_phi)
for i in range(3):
    for j in range(i+1, 3):
        divisors.append(factor_phi[i] * factor_phi[j])

divisors.append(p)
divisors = sorted(divisors)