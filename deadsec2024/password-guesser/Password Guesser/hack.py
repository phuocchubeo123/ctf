from collections import Counter

counts = [5, 4, 7, 5, 5, 8, 9, 4, 5, 7, 4, 4, 7, 5, 7, 8, 4, 2, 5, 5, 4, 3, 10, 4, 5, 7, 4, 4, 4, 6, 5, 12, 5, 5, 5, 8, 7, 9, 2, 3, 2, 5, 8, 6, 4, 4, 7, 2, 4, 5, 7, 9, 4, 9, 7, 4, 7, 8, 4, 2, 4, 4, 4, 4, 3, 3, 7, 4, 6, 9, 4, 4, 4, 6, 7, 4, 4, 4, 1, 3, 5, 8, 4, 9, 11, 7, 4, 2, 4]
c = b'q[\n\x05\xad\x99\x94\xfb\xc1W9\xcb`\x96\xb9|CA\xb8\xb5\xe0v\x93\xff\x85\xaa\xa7\x86\xeas#c'
iv = b'+\xd5}\xd8\xa7K\x88j\xb5\xf7\x8b\x95)n53'

print('Length of count is:', len(counts))
print('Sum of count is:', sum(counts))
print('Minimum of count is:', min(counts))
print(sorted(counts))
cnt2 = sorted(counts)
print('Counter of count is:', Counter(cnt2).items())

max_sum = 100000
num_ans = [[0 for j in range(len(counts))] for i in range(max_sum)]
for i in range(1, max_sum):
    for j in range(len(counts)):
        for k in range(256):
            