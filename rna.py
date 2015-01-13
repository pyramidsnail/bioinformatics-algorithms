import sys, re, os
def rna(s):
    return s.replace('T','U')
if __name__ == '__main__':
    f = open(sys.argv[1],'r')
    line = f.readline().strip()
    print rna(line)
