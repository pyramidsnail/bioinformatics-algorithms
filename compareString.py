import sys, os, re
from collections import defaultdict

sys.setrecursionlimit(2000)


def dpchange(money, coins):
    minnumcoins=[float("inf")]*(money+1)
    minnumcoins[0] = 0
    for i in xrange(1, money+1):
        for j in coins:
            if i >= j:
                if minnumcoins[i-j]+1<minnumcoins[i]:
                    minnumcoins[i] = minnumcoins[i-j]+1
    return minnumcoins[money]


def Manhattan(n, m, down, right):
    length = [[0 for x in xrange(m+1)] for x in xrange(n+1)]
    for i in xrange(1,n+1):
        length[i][0] = length[i-1][0]+down[i-1][0]
    for i in xrange(1,m+1):
        length[0][i] = length[0][i-1]+right[0][i-1]
    for i in xrange(1, n+1):
        for j in xrange(1, m+1):
            length[i][j] = max((length[i-1][j]+down[i-1][j]),(length[i][j-1]+right[i][j-1]))
    return length[n][m]


def lcs(v,w):
    length = [[0 for x in xrange(len(w)+1)] for x in xrange(len(v)+1)]
    for i in xrange(len(v)):
        for j in xrange(len(w)):
            if v[i]==w[j]:
                length[i+1][j+1] = length[i][j]+1
            else:
                length[i+1][j+1] = max(length[i+1][j], length[i][j+1])
    restr = ""
    x, y = len(v), len(w)
    while x!=0 and y!=0:
        if length[x-1][y] == length[x][y]:
            x -= 1
        elif length[x][y-1] == length[x][y]:
            y -= 1
        else:
            restr = v[x-1]+restr
            x -= 1
            y -= 1
    return restr

def toposort(graph):
    from functools import reduce
    data = defaultdict(set)
    for x, y in graph.items():
        for z in y:
            data[z[0]].add(x)
 
    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    # Add empty dependences where needed
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered)
                for item, dep in data.items()
                    if item not in ordered}
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.items())
 
def longestpathDAG(graph, startnode, endnode):
    """http://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/"""
    ### TOPOLOGICALLY SORT THE VERTICES
    order = []
    for part in toposort(graph):
        order.extend(list(part))
    # order.reverse()
 
    ### INITIALIZE DISTANCE MATRIX
    LOWDIST=-99999999999999999
    dist = dict((x, LOWDIST) for x in graph.keys())
    dist[startnode] = 0
 
    ### MAIN PART
    comesfrom = dict()
    for node in order: # u
        for nbr, nbrdist in graph[node]: # v
            if dist[nbr] < dist[node] + nbrdist:
                dist[nbr] = dist[node] + nbrdist
                comesfrom[nbr] = node
 
    ### BACKTRACKING FOR MAXPATH
    maxpath = [endnode]
    while maxpath[-1] != startnode:
        maxpath.append(comesfrom[maxpath[-1]])
    maxpath.reverse()
 
    return dist[endnode], maxpath
def blosum62():
    matrix = {}
    f = open('BLOSUM62.txt','r')
    lines = f.readlines()
    amino = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
    for i in xrange(1,21):
        tmp = lines[i].strip().split()
        for j in xrange(1,21):
            matrix[(amino[i-1],amino[j-1])]=int(tmp[j])
    return matrix

def pam250():
    matrix = {}
    f = open('PAM250.txt','r')
    lines = f.readlines()
    amino = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
    for i in xrange(1,21):
        tmp = lines[i].strip().split()
        for j in xrange(1,21):
            matrix[(amino[i-1],amino[j-1])]=int(tmp[j])
    return matrix

def global_align(x,y,score,indel):
    M = [[0 for i in xrange(len(y)+1)]for i in xrange(len(x)+1)]
    for i in xrange(1,len(x)+1):
        M[i][0] = indel*i
    for i in xrange(1, len(y)+1):
        M[0][i] = indel*i
    for i in xrange(1, len(x)+1):
        for j in xrange(1, len(y)+1):
            M[i][j] = max((M[i-1][j-1]+score[(x[i-1],y[j-1])]),
                          (M[i-1][j]+indel), (M[i][j-1]+indel))

    i, j = len(x), len(y)
    s, t = "", ""
    while i>0 or j>0:
        if M[i][j] == M[i-1][j]+indel:
            s = x[i-1]+s
            t = '-'+t
            i -= 1
        elif M[i][j] == M[i][j-1]+indel:
            s = '-'+s
            t = y[j-1]+t
            j -= 1
        else:
            s = x[i-1]+s
            t = y[j-1]+t
            i -= 1
            j -= 1
    return M[len(x)][len(y)], s, t

def local_align(x,y,score,indel):
    best = 0
    opt = (0,0)
    M = [[0 for i in xrange(len(y)+1)]for i in xrange(len(x)+1)]
    for i in xrange(1, len(x)+1):
        for j in xrange(1, len(y)+1):
            M[i][j] = max((M[i-1][j-1]+score[(x[i-1],y[j-1])]),
                          (M[i-1][j]+indel), (M[i][j-1]+indel), 0)

            if M[i][j]>best:
                best = M[i][j]
                opt = (i,j)
    i, j = opt
    s, t = "", ""
    while (i>0 or j>0) and M[i][j]!=0 :
        if M[i][j] == M[i-1][j]+indel:
            s = x[i-1]+s
            t = '-'+t
            i -= 1
        elif M[i][j] == M[i][j-1]+indel:
            s = '-'+s
            t = y[j-1]+t
            j -= 1
        else:
            s = x[i-1]+s
            t = y[j-1]+t
            i -= 1
            j -= 1
    return best, s, t

def editdistance(x,y):
    M = [[0 for i in xrange(len(y)+1)]for i in xrange(len(x)+1)]
    for i in xrange(1,len(x)+1):
        M[i][0] = (-1)*i
    for i in xrange(1, len(y)+1):
        M[0][i] = (-1)*i
    for i in xrange(1, len(x)+1):
        for j in xrange(1, len(y)+1):
            score = 0 if x[i-1]==y[j-1] else -1
            M[i][j] = max((M[i-1][j-1]+score),
                          (M[i-1][j]-1), (M[i][j-1]-1))
    return -M[len(x)][len(y)]

def fitting_alignment(v, w):
    s = [[0 for i in xrange(len(w+1))] for i in xrange(v+1)]
    backtrack = [[0 for i in xrange(len(w+1))] for i in xrange(v+1)]

    for i in xrange(1,len(v)+1):
        for j in xrange(1, len(w)+1):
            scores = = [s[i-1][j]-1, s[i][j-1]-1,
                          s[i-1][j-1]+1 if v[i-1]==w[j-1] else s[i-1][j-1]+1 ]
            s[i][j] = max(scoresx)
            backtrack[i][j] = scores.index(s[i][j])


if __name__ =="__main__":
    f = open("248_3","r")
    lines = f.readlines()
    x = lines[0].strip()
    y = lines[1].strip()
    print editdistance(x,y)

    
    # f = open('247_9','r')
    # lines = f.readlines()
    # x = lines[0].strip()
    # y = lines[1].strip()
    # # score, s, t = global_align(x, y, blosum62(), -5)
    # score, s, t = local_align(x, y, pam250(), -5)
    # print score
    # print s
    # print t

    
    # f = open("245_7",'r')
    # lines = f.readlines()
    # startnode = int(lines[0].strip())
    # endnode = int(lines[1].strip())
    # graph = {}
    # max_num = 0
    # for i in xrange(2,len(lines)):
    #     start = int(lines[i].strip().split("->")[0])
    #     end = int(lines[i].strip().split("->")[1].split(":")[0])
    #     max_num = max(start, end)
    #     weight = int(lines[i].strip().split("->")[1].split(":")[1])
    #     if start in graph:
    #         graph[start].append((end,weight))
    #     else:
    #         graph[start] =[ (end, weight)]
    #     for i in xrange(max_num+1):
    #         if not i in graph:
    #             graph[i]=[]
    # maxdist, maxpath = longestpathDAG(graph, startnode, endnode)
    # print maxdist
    # maxpath = [str(i) for i in maxpath]
    # print  "->".join(maxpath)
    



    # f = open("245_5","r")
    # lines = f.readlines()
    # v = lines[0].strip()
    # w = lines[1].strip()
    # backtrack = lcs(v,w)
    # print lcs( v, w)

    
    # f = open("261_9", "r")
    # lines = f.readlines()
    # n, m = [int(x) for x in lines[0].strip().split()]
    # down = [[0 for x in xrange(m+1)] for x in xrange(n)]
    # for i in xrange(n):
    #     down[i] = [int(x) for x in lines[i+1].strip().split()]
    # right = [[0 for x in xrange(m)] for x in xrange(n+1)]
    # for i in xrange(n+1):
    #     right[i] = [int(x) for x in lines[n+2+i].strip().split()]
    # print Manhattan(n, m, down, right)
        

    # f = open("243_9","r")
    # lines = f.readlines()
    # money = int(lines[0].strip())
    # coins = [int(x) for x in lines[1].strip().split(",")]
    # print dpchange(money,coins)
