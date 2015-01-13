import sys, re, os
def fibd(n,m):
    res = [0 for x in xrange(n+1)]
    for i in xrange(1, n+1):
        if i==1 or i==2:
            res[i] = 1
        elif i<=m+1:
            res[i]= res[i-1]+res[i-2]
        else:
            res[i]=res[i-1]+res[i-2]-2*res[i-m-1]
    return res[n]
    
if __name__ == '__main__':
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    print fibd(n,m)
    
