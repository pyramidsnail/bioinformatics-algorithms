import sys, re, os
def dna(s):
    return s.count('A'), s.count('C'), s.count('G'), s.count('T')

if __name__ == '__main__':
    f = open('rosalind_dna.txt','r')
    line = f.readline().strip()
    a,c,g,t = dna(line)
    print a,
    print c,
    print g,
    print t
