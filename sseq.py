import sys, os, re
from Bio import SeqIO

handle = open('test','rU')
records = list(SeqIO.parse(handle, 'fasta'))

dna = str(records[0].seq)
sub = str(records[1].seq)

start = 0
for i in sub:
    j = start
    while j<len(dna):
        if i == dna[j]:
            print j+1,
            start = j+1
            break
        else:
            j += 1
