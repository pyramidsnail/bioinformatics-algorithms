import sys, re, os
from Bio import SeqIO

def palindrome(seq):
    rev = ''
    for i in xrange(len(seq)-1, -1, -1):
        if seq[i]=='A':
            rev += 'T'
        elif seq[i]=='T':
            rev += 'A'
        elif seq[i]=='C':
            rev += 'G'
        else:
            rev += 'C'
    if rev == seq:
        return True
    else:
        return False

records = list(SeqIO.parse(open('test','r'), 'fasta'))
seq = str(records[0].seq)

for i in xrange(len(seq)-3):
    for j in xrange(4, 13):
        if i+j<=len(seq) and palindrome(seq[i:i+j]):
            print i+1, j
