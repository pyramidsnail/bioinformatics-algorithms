import sys, os, re, itertools

def perm(n):
    p = range(1, n+1)
    res = list(itertools.permutations(p,n))

    return res

if __name__ == '__main__':
    n = int(sys.argv[1])
    res = perm(n)
    print len(res)
    for i in res:
        for j in i:
            print j,
        print
