import sys, re, os
def revc(s):
    newstr = ''
    for i in xrange(len(s)):
        if s[i]=='A':
            newstr += 'T'
        elif s[i]=='T':
            newstr += 'A'
        elif s[i]=='C':
            newstr += 'G'
        else:
            newstr += 'C'

    return newstr[::-1]
if __name__ == '__main__':
    f = open(sys.argv[1],'r')
    line = f.readline().strip()
    print revc(line) 
