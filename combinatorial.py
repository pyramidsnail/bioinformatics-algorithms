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
    p.append(len(p))
    for i in xrange(len(p)-1):
        if p[i+1]-p[i]!=1:
            count += 1
    return count
        
def chromosome2cycle(chromosome):
    nodes = []
    for j in chromosome:
        if j>0:
            nodes.append(2*j-1)
            nodes.append(2*j)
        else:
            nodes.append(-2*j)
            nodes.append(-2*j-1)
    return nodes

def cycle2chromosome(nodes):
    chromosome = []
    for i in xrange(len(nodes)/2):
        if nodes[2*i+1]>nodes[2*i]:
            chromosome.append(nodes[2*i+1]/2)
        else:
            chromosome.append(-1*nodes[2*i]/2)
    return chromosome

def colorededges(p):
    edges = []
    for i in p:
        nodes = chromosome2cycle(i)
        for j in xrange(len(i)-1):
            edges.append((nodes[2*j+1],nodes[2*j+2]))
        edges.append((nodes[2*len(i)-1], nodes[0]))
    return edges
            
def graph2genome(genomegraph):
    p = []
    nodes = []
    for i in xrange(len(genomegraph)):
        if genomegraph[i][1]<genomegraph[i][0]:
            for j in genomegraph:
                if j[0] < genomegraph[i][0] and j[1]>genomegraph[i][1]:
                    nodes.append(j[0])
                    nodes.append(j[1])
            nodes.insert(0,genomegraph[i][1])
            nodes.append(genomegraph[i][0])
            p.append(cycle2chromosome(nodes))
            nodes = []
    return p

def strongly_connected_components_path(vertices, edges):
    identified = set()
    stack = []
    index = {}
    lowlink = {}

    def dfs(v):
        index[v] = len(stack)
        stack.append(v)
        lowlink[v] = index[v]

        for w in edges[v]:
            if w not in index:
                # For Python >= 3.3, replace with "yield from dfs(w)"
                for scc in dfs(w):
                    yield scc
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w not in identified:
                lowlink[v] = min(lowlink[v], lowlink[w])

        if lowlink[v] == index[v]:
            scc = set(stack[index[v]:])
            del stack[index[v]:]
            identified.update(scc)
            yield scc

    for v in vertices:
        if v not in index:
            # For Python >= 3.3, replace with "yield from dfs(v)"
            for scc in dfs(v):
                yield scc

def tobreakdistance(p,q):
    p_block = []
    for i in p:
        for j in i:
            p_block.append(abs(j))
    q_block = []
    for i in q:
        for j in i:
            q_block.append(abs(j))
    block = len([var1 for var1 in p_block if var1 in q_block])
    p_edge = colorededges(p)
    q_edge = colorededges(q)
    p_edge.extend(q_edge)
    edges = copy.deepcopy(p_edge)
    vertices = []
    directededges = {}
    for i in edges:
        vertices.extend([i[0],i[1]])
        if i[0] not in directededges:
            directededges[i[0]]=[]
        directededges[i[0]].append(i[1])
        if i[1] not in directededges:
            directededges[i[1]]=[]
        directededges[i[1]].append(i[0])
    for i in directededges:
        directededges[i]=list(set(directededges[i]))
    count = 0
    for i in strongly_connected_components_path(vertices, directededges):
        count += 1
    return block-count


def tobreakongenomegraph(genomegraph,i0, i1, j0, j1):
    if (i0, i1) in genomegraph:
        genomegraph.remove((i0, i1))
        ihead = i0
        itail = i1
    else:
        genomegraph.remove((i1, i0))
        ihead = i1
        itail = i0

    if (j0, j1) in genomegraph:
        genomegraph.remove((j0, j1))
        jhead = j0
        jtail = j1

    else:
        genomegraph.remove((j1, j0))
        jhead = j1
        jtail = j0
    genomegraph.append((ihead, jtail))
    genomegraph.append((jhead, itail))

    return genomegraph

def tobreakongenome(p,i0,j0,i1,j1):
    # p is a genome contains list of list
    genomegraph = colorededges(p)
    genomegraph = tobreakongenomegraph(genomegraph,i0,j0,i1,j1)
    res = graph2genome(genomegraph)
    return res
    

if __name__ == '__main__':
    # print graph2genome([(2, 4), (3, 6), (5, 1), (8, 9), (10, 12), (11, 7)])
    # print tobreakongenomegraph([(2,4),(3,8),(7,5),(6,1)], 1, 6, 3,8)
    # print tobreakongenome([[+1,-2,-4,+3]],1,6,3,8)


    f = open('test','r')
    lines = f.readlines()
    graph = lines[0].strip().lstrip('(').rstrip(')')
    graph = graph.split()
    graph = [int(x) for x in graph]
    points = lines[1].strip().split()
    points = [int(x) for x in points]
    print tobreakongenome(graph, points[0],points[1], points[2],points[3])
    

    # f = open('test','r')
    # lines = f.readlines()
    # def buildgenome(line):
    #     genome = []
    #     line = line.strip().rstrip(')').lstrip('(')
    #     items = line.split(')(')
    #     for item in items:
    #         lst = item.split()
    #         lst = [int(x) for x in lst]
    #         genome.append(lst)
    #     return genome
    # p = buildgenome(lines[0])
    # q = buildgenome(lines[1])
    # print tobreakdistance(p,q)

    
    # f = open('dataset_286_3.txt','r')
    # line = f.readline().strip().rstrip(')').lstrip('(')
    # p = line.split()
    # res = greedysorting(p)
    # for i in res:
    #     sys.stdout.write('(')
    #     print ' '.join(i),
    #     sys.stdout.write(')'+'\n')

    # f = open('287_4','r')
    # line = f.readline().strip().rstrip(')').lstrip('(')
    # p = line.split()
    # p = [int(x) for x in p]
    # print breakpoints(p)
