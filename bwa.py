import sys, os, re

def suffixArray(text):
    # text += '$'
    arr = []
    for i in xrange(len(text)):
        arr.append(text[i:])
    arr_sort = sorted(arr)
    for i in arr_sort:
        print str(arr.index(i))+',',

def bwt(text):
    arr = []
    for i in xrange(len(text)):
        arr.append(text[i:]+text[:i])
    arr_sort = sorted(arr)
    res = ''
    for i in xrange(len(arr_sort)):
        res += arr_sort[i][-1]
    print res

def reconstruct(text):
    text = list(text)
    arr = sorted(text)
    while len(arr[0]) != len(text):
        for i in xrange(len(arr)):
           arr[i] = text[i] + arr[i] 
        arr = sorted(arr)
    return arr[0][1:]+'$'


def bwmatching(text, patterns):
if __name__ == '__main__':
    text = open('test', 'r').readline().strip()
    # suffixArray(text)
    # bwt(text)
    print reconstruct(text)
