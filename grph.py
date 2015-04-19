import sys, re, os
from Bio import SeqIO
def prefix(string):
    return string[:3]
def suffix(string):
    return string[len(string)-3:]

for record1 in SeqIO.parse('test', 'fasta'):
    for record2 in SeqIO.parse('test', 'fasta'):
        if suffix(str(record1.seq))==prefix(str(record2.seq)) and str(record1.id) != str(record2.id):
            print record1.id, record2.id
