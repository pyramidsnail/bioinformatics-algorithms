#coding=gbk
#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys, os, re
from collections import defaultdict
from itertools import product

sys.setrecursionlimit(50000)
 

def hamming_distance(text1, text2):
    total = 0
    for i in xrange(len(text1)):
        if text1[i] != text2[i]:
            total += 1
    return total

def neighbors(pattern, d):
    if d==0:
        return set([pattern])
    if len(pattern)==1:
        return set(["A","C","G","T"])
    neighborhood = set([])
    first, suffix = pattern[0], pattern[1::]
    suffix_neighbors = neighbors(suffix, d)
    for text in suffix_neighbors:
        if hamming_distance(suffix,text) < d:
            for nucleotide in 'ACGT':
                neighborhood = neighborhood.union([nucleotide+text])
        else:
            neighborhood = neighborhood.union([first+text])
    return neighborhood

def MotifEnumeration(dna, k, d):
    patterns = set([])
    for i in xrange(len(dna[0])-k):
        kmer = dna[0][i:k+i]
        distance = neighbors(kmer,d)
        for x in distance:
            for m in xrange(1,len(dna)):
                for n in xrange(len(dna[m])-k+1):
                    if hamming_distance(x, dna[m][n:k+n])<=d:
                        break
                    n += 1
                if n ==  len(dna[m])-k+1:
                    break
                m += 1
            if m == len(dna):
                patterns = patterns.union(set([x]))
    return patterns


def kmer(n, seq):
    items = []
    for i in range(len(seq)-n+1):
        items.append(seq[i:i+n])
    return  items


def prefix(str):
    return str[0:len(str)-1]
def suffix(str):
    return str[1:]

def overlap(file):
    f = open(file,"r")
    lines = [line.strip() for line in f.readlines()]
    result = lines[0]
    length = len(lines[0])
    del lines[0]
    i = 0

    while lines:
        if suffix(lines[i])==prefix(result):
            result = lines[i][0]+result
            del lines[i]
            i -= 1
        if prefix(lines[i])==suffix(result):
            result = result+lines[i][length-1]
            del lines[i]
            i -= 1
        i = i+1 if i<len(lines)-1 else 0        
    return result

def overlapGraph(file):
    f = open(file,"r")
    lines = [line.strip() for line in f.readlines()]
    result=[]
    for i  in xrange(len(lines)):
        suf = suffix(lines[i])
        new = lines[:i]+lines[i+1:]
        for item in new:
            if prefix(item) == suf:
                result.append(lines[i]+' -> '+item)
    result.sort()
    return result
        
def debruijn(k, seq):
    node = kmer(k-1, seq)
    result = {}
    for i in xrange(len(node)-1):
        if not node[i] in result:
            result[node[i]]=[]
        if suffix(node[i])==prefix(node[i+1]):
            result[node[i]].append(node[i+1])
    output=[]
    for i in sorted(result):
        output.append(i+' -> '+",".join(result[i]))
    return output


def debruijnPattern(patterns):
    setPattern = []
    for i in patterns:
        setPattern.append(prefix(i))
        setPattern.append(suffix(i))
    setPattern = list(set(setPattern))
    result = {}
    for i in setPattern:
        if not i in result:
            result[i] = []
        for j in setPattern:
            if suffix(i) == prefix(j):
                result[i].append(j)

    output=[]
    for i in sorted(result):
        output.append(i+' -> '+",".join(result[i]))
    return output

def find_eulerian_tour(graph, start_node):             
    def freqencies():
        my_list = [x for (x, y) in graph]
        result = [0 for i in range(max(my_list) + 1)]
        for i in my_list:
            result[i] += 1
        return result
         
    def find_node(tour):
        for i in tour:
            if freq[i] != 0:
                return i
        return -1
     
    def helper(tour, next):
        find_path(tour, next)
        u = find_node(tour)
        while sum(freq) != 0:     
            sub = find_path([], u)
            tour = tour[:tour.index(u)] + sub + tour[tour.index(u) + 1:]  
            u = find_node(tour)
        return tour
                  
    def find_path(tour, next):
        for (x, y) in graph:
            if x == next:
                current = graph.pop(graph.index((x,y)))
                graph.pop(graph.index((current[1], current[0])))
                tour.append(current[0])
                freq[current[0]] -= 1
                freq[current[1]] -= 1
                return find_path(tour, current[1])
        tour.append(next)
        return tour             
              
    # graph += [(y, x) for (x, y) in graph]
    freq = freqencies()   
    return helper([], start_node)

def eulerian_path(graph):
    # find the start and end point
    inout = {}
    for (x,y) in graph:
        if not x in inout:
            inout[x] = 0
        if not y in graph:
            inout[y] = 0
        inout[x] += 1
        inout[y] += -1
    for key, value in inout.iteritems():
        if value == -1:
            start = key
    # find the tour
    tour = []
    current_vertex = start
    tour.append(current_vertex)
    while len(graph)>0:
        for edge in graph:
            if current_vertex == edge[0]:
                current_vertex = edge[1]
                graph.remove(edge)
                tour.append(current_vertex)
                break
    return tour
        
def find_start_end(graph):
    inout = {}
    for (x,y) in graph:
        if not x in inout:
            inout[x] = 0
        if not y in inout:
            inout[y] = 0
        inout[x] += 1
        inout[y] += -1
    result = [0,0]
    for key, value in inout.iteritems():
        if value == 1:
            result[0] = key
        if value == -1:
            result[1] = key
    return result

def take_tour(graph, node_start=None):
    if len(graph) == 0:
        if node_start is None:
            return []
        return [node_start]

    node_start = graph[0][0] if node_start is None else node_start

    for chosen_edge in [x for x in graph if node_start == x[0]]:
        (node_a, node_b) = chosen_edge
        path = take_tour([e for e in graph if e != chosen_edge],
                         node_b)
        if path is not False:
            return [node_start] + path
    return False

def find_euler_tour(graph, start_node):
    tour = []
    E = graph

    numEdges = defaultdict(int)

    def find_tour(u):
        for e in E:
            if u == e[0]:
                u,v = e
                E.remove(e)
                find_tour(v)
        tour.insert(0,u)

    current = start_node
    find_tour(current)
    return [tour,E]


def euler_tour(E, tour, start_node):
        while len(E)!=0:
            if start_node:
                start_node = start_node
            else:
                for node in tour:
                    find_node = False
                    for (i, j) in E:
                        if node == i:
                            start_node = node
                            find_node = True
                            break
                    if find_node:
                        break
            add_tour, E = find_euler_tour(E, start_node)
            if len(tour) == 0:
                tour = add_tour
            else:
                tour = tour[:tour.index(add_tour[0])]+add_tour+tour[tour.index(add_tour[0])+1:]
            start_node = None
        return tour
def universal(k):
    kmerset = [''.join(p) for p in product('01', repeat=k)]
    graph=[]
    for i in xrange(len(kmerset)):
        #if prefix(kmerset[i])!=suffix(kmerset[i]):
        graph.append((prefix(kmerset[i]), suffix(kmerset[i]))) 
    # (start_node, end_node)=find_start_end(graph)
    graph = list(set(graph))
    result = euler_tour(graph, [], graph[0][0])
    sys.stdout.write(result[0])
    for i in xrange(1,len(result)-k+1):
        sys.stdout.write(result[i][-1])


    

if __name__ == '__main__':
    # f = open("203_5","r")
    # lines = [line.strip() for line in f.readlines()]
    # graph = []
    # for line in lines:
    #     start = line.split(" -> ")[0]
    #     ends =  line.split(" -> ")[1].split(",")
    #     for item in ends:
    #         graph.append((int(start), int(item)))
    
    # (start,end) = find_start_end(graph)
    # # graph.append((int(end),int(start)))
    # result = euler_tour(graph, [], int(start))
    # #print "->".join(result)+"->"+str(result[0])
    # for i in xrange(len(result)-1):
    #     sys.stdout.write(str(result[i])+"->")
    # sys.stdout.write(str(result[-1]))

    # f = open("203_6","r")
    # lines = [line.strip() for line in f.readlines()  ]
    universal(9)
    
