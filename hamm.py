import sys, re, os
def hamm(v,w):
    count = 0
    for i in xrange(len(v)):
        if v[i]!=w[i]:
            count += 1
    return count

if __name__ == '__main__':
    v = raw_input()
    w = raw_input()
    print hamm(v,w)
