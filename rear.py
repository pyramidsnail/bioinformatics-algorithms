import re, sys, os

seq1 = [x for x in raw_input().split()]
seq2 = [x for x in raw_input().split()]


# def get_permutation(L1, L2):
#     """Find permutation that converts L1 into L2.

#     See http://en.wikipedia.org/wiki/Cycle_representation#Notation
#     """
#     if sorted(L1) != sorted(L2):
#         raise ValueError("L2 must be permutation of L1 (%s, %s)" % (L1,L2))

#     permutation = map(dict((v, i) for i, v in enumerate(L1)).get, L2)
#     assert [L1[p] for p in permutation] == L2
#     return permutation

# def number_of_swaps(permutation):
#     """Find number of swaps required to convert the permutation into
#     identity one.

#     """
#     # decompose the permutation into disjoint cycles
#     nswaps = 0
#     seen = set()
#     for i in xrange(len(permutation)):
#         if i not in seen:           
#            j = i # begin new cycle that starts with `i`
#            while permutation[j] != i: 
#                j = permutation[j]
#                seen.add(j)
#                nswaps += 1

#     return nswaps

# perm = get_permutation(seq1, seq2)
# print number_of_swaps(perm)

count = 0

for i in xrange(len(seq2)):
    if seq1[i]!=seq2[i]:
        index = seq2.index(seq1[i])
        for x in xrange(i, index+1):
            
            tmp = seq2[x]
            seq2[x] = seq2[i+index-x]
            seq2[i+index-x] = tmp
            
        count += 1

print count 
