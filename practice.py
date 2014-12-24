#coding=gbk
#coding=utf-8
#-*- coding: UTF-8 -*- 

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
    for x in sorted(items):
        print x

def overlap(file):
    f = open(file,"r")
    lines = [line.strip() for line in f.readlines()]
    result = lines[0]
    length = len(lines[0])
    del lines[0]
    def prefix(str):
        return str[0:length-1]
    def suffix(str):
        return str[len(str)-length+1:]
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
if __name__ == '__main__':
    print overlap("dataset_198_3.txt")
    
