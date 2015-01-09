import sys, os, re, itertools

def perm(p,n):
    res = list(itertools.product(range(len(p)),repeat=n))
    res.sort()
    resstr = []
    for i in xrange(len(res)):
        resstr.append('')
        for j in res[i]:
            resstr[i] += p[j]
            
            
    return resstr

if __name__ == '__main__':
    p = raw_input().strip().split()
    n = int(raw_input())
    res = perm(p, n)
    for i in res:
        print i
