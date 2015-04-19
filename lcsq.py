import sys, re, os
from Bio import SeqIO

records = list(SeqIO.parse(open('test','rU'),'fasta'))
seq1 = str(records[0].seq)
seq2 = str(records[1].seq)

lcs = [[0 for x in xrange(len(seq2)+1)] for x in xrange(len(seq1)+1)]

for i in xrange(len(seq1)+1):
    for j in xrange(len(seq2)+1):
        if i==0 or j==0:
            lcs[i][j] = 0
        elif seq1[i-1] == seq2[j-1]:
            lcs[i][j] = lcs[i-1][j-1]+1
        else:
            lcs[i][j] = max(lcs[i-1][j],lcs[i][j-1])

i = len(seq1)
j = len(seq2)
seq = ''
while i>0 and j>0:
    if seq1[i-1] == seq2[j-1]:
        seq = seq1[i-1]+seq
        i -= 1
        j -= 1
    elif lcs[i-1][j]>lcs[i][j-1]:
        i -= 1
    else:
        j -= 1

print seq
