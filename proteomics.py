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

def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in set(graph[start]) - set(path):
        for i in dfs_paths(graph, next, goal, path + [next]):
            yield i

def find_all_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in graph[start]:
        for i in find_all_paths(graph, next, goal, path+[next]):
            yield i


def find_max_paths(graph):
    '''
    takes too much time to build the DAG
    '''
    return 
    
    
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

def toposort(graph, unvisit):
    for node in graph:
        if node in unvisit:
            sort(graph, node)
        
def peptide_sequencing(spectrum):
    spectrum = [int(x) for x in spectrum]
    graph = dict((i,[]) for i in xrange(len(spectrum)))
    # graph[0] = []
    
    for i in xrange(len(spectrum)):
        for j in mass.values():
            if i+j<len(spectrum):
                graph[i].append(i+j)

    # spectrum.insert(0,0)
    # paths = bfs_paths(graph, 0, len(spectrum)-1)
    paths = dfs_paths(graph, 0, len(spectrum)-1)
    max_value = -1000000000
    max_path = []
    for path in paths:
        total = 0
        for i in path:
            total += spectrum[i]
        if total>max_value:
            max_value = total
            max_path = path

    seq = ''
    for i in xrange(1, len(max_path)):
        seq += mass.keys()[mass.values().index(max_path[i]-max_path[i-1])]
        

    return seq
    

def peptide_identification(spectrum, proteome):
    '''
    spectrum = [int(x) for x in spectrum]
    graph = dict((i,[]) for i in xrange(len(spectrum)))
    
    for i in xrange(len(spectrum)):
        for j in mass.values():
            if i+j<len(spectrum):
                graph[i].append(i+j)

    # paths = dfs_paths(graph, 0, len(spectrum)-1)
    paths = find_all_paths(graph, 0, len(spectrum)-1)
    max_value = -1000000000
    max_path = []
    max_seq = ''
    for path in paths:
        total = 0
        seq = ''
        for i in xrange(1, len(path)):
            seq += mass.keys()[mass.values().index(path[i]-path[i-1])]
        if seq in proteome:

            for i in path:
                total += spectrum[i]
            if total>max_value:
                max_value = total
                max_path = path
                max_seq = seq
        

    return max_seq, max_value
    '''
    length = len(proteome)
    max_value = -1000000000
    max_seq = ''
    for i in xrange(length):
        for j in xrange(i+1, length):
            if weight(proteome[i:j+1]) == len(spectrum):
                if peptide_score(proteome[i:j+1], spectrum) > max_value:
                    max_value = peptide_score(proteome[i:j+1], spectrum)
                    max_seq = proteome[i:j+1]
            if weight(proteome[i:j+1]) > len(spectrum):
                break


    return max_seq
            
        
def peptide_identification_subs(spectrum, subs):
    # length = len(proteome)
    # subs = [proteome[i:j+1] for i in xrange(length) for j in xrange(i,length)]
    max_value = -1000000000
    max_seq = ''

    for sub in subs:
        if peptide_score(sub, spectrum) > max_value:
            max_value = peptide_score(sub, spectrum)
            max_seq = sub
    return max_seq, max_value
    
def weight(seq):
    total = 0
    for i in seq:
        total += mass[i]
    return total

def peptide_score(seq, spectrum):
    value = 0
    index = -1
    for i in seq:
        index += mass[i]
        value += int(spectrum[index])
    return value
        

    
def PSMSearch(spectral_vectors, proteome, threshold):
    PSMSet = []
    length = len(proteome)
    vector_length = []
    for i in spectral_vectors:
        vector_length.append(len(i.strip().split()))
    # subs = [proteome[i:j+1] for i in xrange(length) for j in xrange(i,length)]
    sub_weight = dict((i,[]) for i in vector_length)
    for i in xrange(length):
        for j in xrange(i+1, length):
            if weight(proteome[i:j+1]) in vector_length:
                sub_weight[weight(proteome[i:j+1])].append(proteome[i:j+1])
            if weight(proteome[i:j+1]) > max(vector_length):
                break
    # for i in subs:
    #     if weight(i) not in sub_weight:
    #         sub_weight[weight(i)] = []
    #     sub_weight[weight(i)].append(i)
    
    for vector in spectral_vectors:
        vector = vector.strip().split()
        if len(vector) in sub_weight:
            seq, value = peptide_identification_subs(vector, sub_weight[len(vector)])
            if value >= threshold:
                PSMSet.append(seq)
    return PSMSet


def spectral_dic_size(spectrum, threshold, max_score):
    spectrum.insert(0,0)
    min_score = 0
    for i in spectrum:
        if i<0:
            min_score += i

    size = dict((x,[0]*len(spectrum)) for x in xrange(min_score, max_score+1))
    size[0][0] = 1
    for i in xrange(len(spectrum)):
        for score in size.keys():
            for j in mass.values():
                if i-j>=0 and (score-spectrum[i]) in size:
                    size[score][i] += size[score-spectrum[i]][i-j]

    total = 0
    for i in xrange(threshold, max_score+1):
        total += size[i][len(spectrum)-1]

    return total

def spectral_dic_prob(spectrum, threshold, max_score):
    spectrum.insert(0,0)

    min_score = 0
    for i in spectrum:
        if i<0:
            min_score += i

    prob = dict((x,[0]*len(spectrum)) for x in xrange(min_score, max_score+1))
    prob[0][0] = 1
    for i in xrange(len(spectrum)):
        for score in prob.keys():
            for j in mass.values():
                if i-j>=0 and (score-spectrum[i]) in prob:
                    prob[score][i] += 0.05*prob[score-spectrum[i]][i-j]

    total = 0
    for i in xrange(threshold, max_score+1):
        total += prob[i][len(spectrum)-1]

    return total



    
    
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
                
   # f = open('test', 'r')
   # vector = f.readline().strip().split()
   # print peptide(vector)


   # f = open('test', 'r')
   # spectrum = f.readline().strip().split()
   # print peptide_sequencing(spectrum)


   # f = open('test', 'r')
   # spectrum = f.readline().strip().split()
   # proteome = f.readline().strip() 
   # print peptide_identification(spectrum, proteome)

   # f = open('test', 'r')
   # lines = f.readlines()
   # spectral_vectors = lines[0:len(lines)-2]
   # proteome = lines[-2].strip()
   # threshold = int(lines[-1])
   # PSMSet = PSMSearch(spectral_vectors, proteome, threshold)
   # for i in PSMSet:
   #     print i


   f = open('test', 'r')
   lines = f.readlines()
   spectrum = [int(x) for x in lines[0].strip().split()]
   threshold = int(lines[1])
   max_score = int(lines[2])
   # print spectral_dic_size(spectrum, threshold, max_score)
   print spectral_dic_prob(spectrum, threshold, max_score)
