import sys, os, re

codon = {'UUU': 'F',
         'UUC': 'F',
         'UUA': 'L',
         'UUG': 'L',
         'UCU': 'S',
         'UCC': 'S',
         'UCA': 'S',
         'UCG': 'S',
         'UAU': 'Y',
         'UAC': 'Y',
         'UGU': 'C',
         'UGC': 'C',
         'UGG': 'W',
         'CUU': 'L',
         'CUC': 'L',
         'CUA': 'L',
         'CUG': 'L',
         'CCU': 'P',
         'CCC': 'P',
         'CCA': 'P',
         'CCG': 'P',
         'CAU': 'H',
         'CAC': 'H',
         'CAA': 'Q',
         'CAG': 'Q',
         'CGU': 'R',
         'CGG': 'R',
         'CGC': 'R',
         'CGA': 'R',
         'AUU': 'I',
         'AUC': 'I',
         'AUA': 'I',
         'AUG': 'M',
         'ACU': 'T',
         'ACC': 'T',
         'ACA': 'T',
         'ACG': 'T',
         'AAU': 'N',
         'AAC': 'N',
         'AAA': 'K',
         'AAG': 'K',
         'AGU': 'S',
         'AGC': 'S',
         'AGA': 'R',
         'AGG': 'R',
         'GUU': 'V',
         'GUC': 'V',
         'GUA': 'V',
         'GUG': 'V',
         'GCU': 'A',
         'GCC': 'A',
         'GCA': 'A',
         'GCG': 'A',
         'GAU': 'D',
         'GAC': 'D',
         'GAA': 'E',
         'GAG': 'E',
         'GGU': 'G',
         'GGC': 'G',
         'GGA': 'G',
         'GGG': 'G'         
    }


f = open('test','rU')
lines = f.readlines()
for i in xrange(len(lines)):
    if i == 1:
        dnaseq = lines[i].strip()
    elif i%2 == 1:
        intron = lines[i].strip()
        dnaseq=dnaseq.replace(intron, '')


rnaseq1 = ''
rnaseq2 = dnaseq.replace('T','U')
for i in dnaseq:
    if i == 'A':
        rnaseq1 += 'U'
    elif i == 'T':
        rnaseq1 += 'A'
    elif i == 'C':
        rnaseq1 += 'G'
    else:
        rnaseq1 += 'C'


prot = ''

if rnaseq1[0:3] == 'AUG':
    rnaseq = rnaseq1
else:
    rnaseq = rnaseq2
for i in xrange(0, len(rnaseq),3):
    if rnaseq[i:i+3] in codon:
        prot += codon[rnaseq[i:i+3]]
    else:
        break
    
print prot    

# for i in xrange(len(rnaseq1)):
#     if rnaseq1[i:i+3]=='AUG':
#         for j in xrange(i, len(rnaseq1),3):
#             if rnaseq1[j:j+3] in codon:
#                 prot += codon[rnaseq1[j:j+3]]
#             else:
#                 break
#         print prot

# prot = ''
# for i in xrange(len(rnaseq2)):
#     if rnaseq2[i:i+3]=='AUG':
#         for j in xrange(i, len(rnaseq2),3):
#             if rnaseq2[j:j+3] in codon:
#                 prot += codon[rnaseq2[j:j+3]]
#             else:
#                 break
#         print prot


#         exit
