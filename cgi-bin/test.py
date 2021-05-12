a = [1230, 1230, 100]

from collections import Counter

multis = {}
for index, item in enumerate(a):
    multis[index] = item

print(multis)

multis = dict(Counter(multis.values()))

print(multis)