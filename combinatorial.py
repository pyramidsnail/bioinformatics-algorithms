import sys, os, re, copy
from string import maketrans

def ksorting(p, i, k):
    transtab = maketrans('+-','-+')
    newp = copy.deepcopy(p)
    for j in xrange(i, k+1):
        newp[j] = p[k+i-j].translate(transtab)
    return newp

def greedysorting(p):
    proc = []
    p = list(p)
    for i in xrange(len(p)):
        if p[i]!='+'+str(i+1) and p[i]!='-'+str(i+1):
            if '+'+str(i+1) in p:
                k = p.index('+'+str(i+1))
            else:
                k = p.index('-'+str(i+1))
            p = copy.deepcopy(ksorting(p, i, k))
            proc.append(p)
                

        if p[i]=='-'+str(i+1):
            newp = copy.deepcopy(p)
            newp[i] = '+'+str(i+1)
            proc.append(newp)
            p = copy.deepcopy(newp)

    return proc
def breakpoints(p):
    count = 0
    p.insert(0, 0)
    p.append(len(p)+1)
    for i in xrange(len(p)+1):
        if p[i+1]-p[1]!=1:
            count += 1
    return count
        
            
            
if __name__ == '__main__':
    # f = open('dataset_286_3.txt','r')
    # line = f.readline().strip().rstrip(')').lstrip('(')
    # p = line.split()
    # res = greedysorting(p)
    # for i in res:
    #     sys.stdout.write('(')
    #     print ' '.join(i),
    #     sys.stdout.write(')'+'\n')
    f = open('dataset_286_3.txt','r')
    line = f.readline().strip().rstrip(')').lstrip('(')
    p = line.split()
    p = [int(x) for x in p]
    print breakpoints(p)
