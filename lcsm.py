import sys, os, re
from Bio import SeqIO

def get_all_substrings(input_string):
  length = len(input_string)
  return [input_string[i:j+1] for i in xrange(length) for j in xrange(i,length)]

handle = open('test', 'rU')
lst = []
for record in SeqIO.parse(handle, 'fasta'):
    lst.append(str(record.seq))


# pool = []
res = set(get_all_substrings(lst[0]))
# for j in res:
#     if j in lst[1]:
#         res.append(j)
# res = set(res)

for i in xrange(len(lst)):
    substrings = get_all_substrings(lst[i])
    # for j in substrings:
    #     if j in lst[i+1]:
    #         pool.append(j)
            
    res &=  set(substrings)
    # pool = []

seqs = ''
for i in res:
    if len(i)>len(seqs):
        seqs = i
print seqs
