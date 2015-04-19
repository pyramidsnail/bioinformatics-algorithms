from Bio import SeqIO
from itertools import product
import re

handle = open('test', 'rU')
for i in SeqIO.parse(handle, 'fasta'):
    seq = str(i.seq)


kmer = list(product('ACGT', repeat=4))
kmer.sort()
for i in kmer:
    substr = ''
    for j in i:
        substr += j
    
    print len(re.findall(r'(?=(%s))' % re.escape(substr), seq)),
