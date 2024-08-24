from hashlib import sha256

m = sha256()
# m.update(b"abc")
# print(m.hexdigest())

# m.update(b"de")
# print(m.hexdigest())

m.update(b"abcde")
print(m.hexdigest())