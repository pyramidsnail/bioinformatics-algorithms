from itertools import permutations
from itertools import combinations

n = int(raw_input())

result_lst = []
tmp1 = list(permutations(range(1, n+1), n))
for x in tmp1:
    for i in xrange(n+1):
        tmp2 = [1]*i+[-1]*(n-i)
        per = set(list(permutations(tmp2,n)))
        for j in per:
            inter = []
            for k in xrange(n):
                inter.append(x[k]*j[k])
            result_lst.append(inter)


print len(result_lst)
for i in result_lst:
    for j in i:
        print j,
    print 

