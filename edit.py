import sys, re, os
from Bio import SeqIO

records = list(SeqIO.parse(open('test','rU'),'fasta'))
seq1 = str(records[0].seq)
seq2 = str(records[1].seq)

distance = [[0 for x in xrange(len(seq2)+1)] for x in xrange(len(seq1)+1)]
for i in xrange(len(seq1)+1):
    for j in xrange(len(seq2)+1):
        if i==0 or j==0:
            distance[i][j] = i+j
        elif seq1[i-1] != seq2[j-1]:
            distance[i][j] = min(distance[i-1][j-1], distance[i-1][j], distance[i][j-1])+1
        elif seq1[i-1] == seq2[j-1]:
            distance[i][j] = distance[i-1][j-1]

print distance[len(seq1)][len(seq2)]
        


