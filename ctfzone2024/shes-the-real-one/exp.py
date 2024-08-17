for u in range(2, 15):
    print('Analysing', u)

    x, y = 1, 2

    for b in bin(u)[3:]:
        if b == "0":
            x, y = 2*x, x+y
        else:
            x, y = x+y, 2*y

        print(x, y)

    print()