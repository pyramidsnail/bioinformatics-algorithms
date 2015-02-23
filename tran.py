import sys, re, os
from Bio import SeqIO

records = list(SeqIO.parse(open('test','rU'),'fasta'))
seq1 = str(records[0].seq)
seq2 = str(records[1].seq)
transition = 0
transversion = 0
nine = ['A','G']
sine = ['C','T']

for i in xrange(len(seq1)):
    if seq1[i]==seq2[i]:
        pass
    elif (seq1[i] in nine and seq2[i] in nine)\
         or (seq1[i] in sine and seq2[i] in sine):
        transition += 1
    else:
        transversion += 1
print 1.0*transition/transversion
    
