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

s = ''
t = ''
i = len(seq1)
j = len(seq2)
while i>0 and j>0:
    if distance[i-1][j-1]==min(distance[i][j-1],distance[i-1][j],distance[i-1][j-1]):
        s = seq1[i-1]+s
        t = seq2[j-1]+t
        i -= 1
        j -= 1
    elif distance[i-1][j]==min(distance[i][j-1],distance[i-1][j],distance[i-1][j-1]):
        s = seq1[i-1]+s
        t = '-'+t
        i -= 1
    elif distance[i][j-1]==min(distance[i-1][j],distance[i][j-1],distance[i-1][j-1]):
        s = '-'+s
        t = seq2[j-1]+t
        j -= 1

print s
print t
