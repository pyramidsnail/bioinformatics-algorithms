import sys, os, re

mass = {'G':57,
        'A':71,
        'S':87,
        'P':97,
        'V':99,
        'T':101,
        'C':103,
        'I':113,
        'L':113,
        'N':114,
        'D':115,
        'K':128,
        'Q':128,
        'E':129,
        'M':131,
        'H':137,
        'F':147,
        'R':156,
        'Y':163,
        'W':186,
        'X':4,
        'Z':5}

def construct_graph(spectrum):
    res = {}
    spectrum.insert(0,0)
    spectrum.sort()
    for i in xrange(len(spectrum)):
        for j in xrange(i+1, len(spectrum)):
            if spectrum[j]-spectrum[i] in mass.values():
                res[(spectrum[i], spectrum[j])] =mass.keys()[mass.values().index(spectrum[j]-spectrum[i])]
                # res.append("%d->%d:%s" %(spectrum[i], spectrum[j],
                           # mass.keys()[mass.values().index(spectrum[j]-spectrum[i])]))
    return res


def find_path(graph, start, end, path):
    path.append(start)
    if start == end:
        return path
    if not start in graph:
        return None
    for node in graph[start]:
        if node not in path:
            return find_path(graph, node, end, path)
    return None

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in set(graph[vertex]) - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def idealSpectrum(seq):
    res = [0]
    pre = 0
    for i in xrange(len(seq)):
        pre += mass[seq[i]]
        res.append(pre)
    suf = 0
    seq_re = seq[::-1]
    for i in xrange(len(seq_re)):
        suf += mass[seq_re[i]]
        res.append(suf)
    return list(set(res))
        
def decoding(spectrum):
    res = construct_graph(spectrum)
    graph = {}
    for key in res:
        if key[0] not in graph:
            graph[key[0]] = []
        graph[key[0]].append(key[1])
    start = 0
    end = max(spectrum)

    paths = bfs_paths(graph, start, end)
    for path in paths:
        seq = ''
        for i in xrange(1, len(path)):
            seq += mass.keys()[mass.values().index(path[i]-path[i-1])]
        if sorted(idealSpectrum(seq)) == sorted(spectrum):
            return seq


def peptide_vector(seq):
    prefix = []
    total = 0
    for i in seq:
        total += mass[i]
        prefix.append(total)
    # prefix.sort()
    res = []
    for i in xrange(max(prefix)):
        if i+1 in prefix:
            res.append(1)
        else:
            res.append(0)
    return res


def peptide(vector):
    seq = ''
    first = -1
    for i in xrange(len(vector)):
        if int(vector[i]) == 1:
            seq += mass.keys()[mass.values().index(i-first)]
            first = i

    return seq
        

if __name__ == '__main__':
    # f = open('test', 'r')
    # spectrum = f.readline().strip().split()
    # spectrum = [int(x) for x in spectrum]
    # res = construct_graph(spectrum)
    # for i in res:
    #     s = "%d->%d:%s" %(i[0], i[1], res[i])
    #     print s
                

    # f = open('test', 'r')
    # spectrum = f.readline().strip().split()
    # spectrum = [int(x) for x in spectrum]
    # print decoding(spectrum)

    # f = open('test', 'r')
    # seq = f.readline().strip()
    # res = peptide_vector(seq)
    # for i in res:
    #     print i,
                
   f = open('test', 'r')
   vector = f.readline().strip().split()
   print peptide(vector)
