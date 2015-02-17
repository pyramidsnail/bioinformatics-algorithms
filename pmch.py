import sys, os,re
import math

seq = raw_input().strip()
counta = 0
countc = 0
for i in xrange(len(seq)):
    if seq[i]=='A':
        counta += 1
    if seq[i]=='C':
        countc += 1
        
    # for j in xrange(i+1, len(seq)):
    #     if (seq[i]=='C' and seq[j]=='G') or \
    #        (seq[i]=='G' and seq[j]=='C') or \
    #        (seq[i]=='A' and seq[j]=='U') or \
    #        (seq[i]=='U' and seq[j]=='A'):
    #         count += 1
# if (seq[0]=='C' and seq[-1]=='G') or \
#        (seq[0]=='G' and seq[-1]=='C') or \
#        (seq[0]=='A' and seq[-1]=='U') or \
#        (seq[0]=='U' and seq[-1]=='A'):
#     count += 1
print math.factorial(counta)*math.factorial(countc)
    
