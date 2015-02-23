from itertools import *
from math import factorial

n, k = [int(x) for x in raw_input().split()]

print (factorial(n)/factorial(n-k))%1000000


# tmp = list(combinations([x for x in range(n)],k))
# count1 = len(list(combinations([x for x in range(n)],k)))
# count2 = len(list(permutations([x for x in range(k)],k)))

# print ((count1%1000000)*(count2%1000000))%1000000
