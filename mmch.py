import sys, os, re
from math import factorial

seq = raw_input().strip()
acount = 0
ucount = 0
ccount = 0
gcount = 0

for i in seq:
    if i == 'A':
        acount += 1
    elif i == 'U':
        ucount += 1
    elif i == 'C':
        ccount += 1
    else:
        gcount += 1

fi = (factorial(max(acount, ucount))/factorial(abs(acount-ucount)))* (factorial(max(ccount, gcount))/factorial(abs(ccount-gcount)))

print fi

