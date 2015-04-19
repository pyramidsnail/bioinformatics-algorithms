import sys, re, os

from Bio import SeqIO
seqs = []

handle = open('test', 'rU')
for record in SeqIO.parse(handle, 'fasta'):
    seqs.append(record.seq)
handle.close()

cols = len(seqs[0])
nc = {'A':[], 'T':[], 'C':[], 'G':[]}
for i in xrange(cols):
    anum = 0
    tnum = 0
    cnum = 0
    gnum = 0
    for j in xrange(len(seqs)):
        if seqs[j][i] == 'A':
            anum += 1
        elif seqs[j][i] == 'T':
            tnum += 1
        elif seqs[j][i] == 'C':
            cnum += 1
        else:
            gnum += 1
    nc['A'].append(anum)
    nc['T'].append(tnum)
    nc['C'].append(cnum)
    nc['G'].append(gnum)

res = ''
for i in xrange(cols):
    maxnum = 0
    maxnc = 'A'
    for key in nc:
        if nc[key][i]>maxnum:
            maxnc = key
            maxnum = nc[key][i]
    res += maxnc

print res
for i in sorted(nc):
    print i+':',
    nc[i] = [str(x) for x in nc[i]]
    print ' '.join(nc[i])
        
        
    
