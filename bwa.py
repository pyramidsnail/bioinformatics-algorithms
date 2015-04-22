import sys, os, re

def suffixArray(text):
    # text += '$'
    arr = []
    for i in xrange(len(text)):
        arr.append(text[i:])
    arr_sort = sorted(arr)
    res = []
    for i in arr_sort:
        res.append(arr.index(i))
    return res

def bwt(text):
    arr = []
    for i in xrange(len(text)):
        arr.append(text[i:]+text[:i])
    arr_sort = sorted(arr)
    res = ''
    for i in xrange(len(arr_sort)):
        res += arr_sort[i][-1]
    return res

def reconstruct(text):
    text = list(text)
    arr = sorted(text)
    while len(arr[0]) != len(text):
        for i in xrange(len(arr)):
           arr[i] = text[i] + arr[i] 
        arr = sorted(arr)
    return arr[0][1:]+'$'


def lasttofirst(bwttext, lastindex):
    symbol = bwttext[lastindex]
    occur = 0
    for i in xrange(lastindex+1):
        if bwttext[i] == symbol:
            occur += 1
    first_col = sorted(bwttext)
    res = 0
    for i in xrange(len(bwttext)):
        if first_col[i] == symbol:
            occur -= 1
        if occur == 0:
            res = i
            break
    return res
    
        
        
    

def bwmatching(text, pattern):
    last = list(text)
    first = sorted(last)
    top = 0
    bottom = len(text)-1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:len(pattern)-1]
            if symbol in last[top:bottom+1]:
                topindex = top+last[top:bottom+1].index(symbol)
                last_reverse = last[top:bottom+1][::-1]
                bottomindex = bottom-last_reverse.index(symbol)
                top = lasttofirst(last, topindex)
                bottom = lasttofirst(last, bottomindex)
            else:
                return 0
        else:
            return bottom-top+1


def firstOccurrence(text):
    dic = {}
    text = sorted(list(text))
    for i in xrange(len(text)):
        if text[i] not in dic:
            dic[text[i]] = i
    return dic

def countTable(text):
    dic = {}
    for i in xrange(len(text)):
        if text[i] not in dic:
            dic[text[i]] = [0]*(len(text)+1)
            for j in xrange(i+1,len(text)+1):
                dic[text[i]][j] = 1
        else:
            for j in xrange(i+1, len(text)+1):
                dic[text[i]][j] += 1
    return dic

def bwtmatching_fast(text, pattern, first_occurrence, countTable):
#     first_occurrence = firstOccurrence(text)
#     count_table = countTable(text)
    last = list(text)
    first = sorted(last)
    top = 0
    bottom = len(text)-1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:len(pattern)-1]
            top = first_occurrence[symbol]+count_table[symbol][top]
            bottom = first_occurrence[symbol]+count_table[symbol][bottom+1]-1
            
        else:
            return bottom-top+1
    return 0
def bwtmatching_fast_location(text, pattern, first_occurrence, count_table):
    last = list(text)
    first = sorted(last)
    top = 0
    bottom = len(text)-1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:len(pattern)-1]
            top = first_occurrence[symbol]+count_table[symbol][top]
            bottom = first_occurrence[symbol]+count_table[symbol][bottom+1]-1
            
        else:
            return (top, bottom)
    return

def bwtlocation(text, pattern,first_occurrence, count_table, suffix):
    loc = []
    if bwtmatching_fast_location(text, pattern, first_occurrence, count_table):

        top, bottom = bwtmatching_fast_location(text, pattern, first_occurrence, count_table)
        for i in xrange(top, bottom+1):
            loc.append(suffix[i])
    return loc



# def bwtmatching_error(text, pattern, first_occurrence, count_table, suffix):
    


if __name__ == '__main__':
    ##### location of the matches
    
    # f = open('test','r')
    # lines = f.readlines()
    # text = lines[0].strip()
    # text += '$'
    # suffix = suffixArray(text)
    # text = bwt(text)

    # res = []
    # first_occurrence = firstOccurrence(text)
    # count_table = countTable(text)

    # for i in lines[1:]:
    #     res.extend(bwtlocation(text, i.strip(),first_occurrence, count_table, suffix))
    # for i in sorted(res):
    #     print i,
    



    # ####### number of matches
    f = open('test', 'r')
    lines = f.readlines() 
    text = lines[0].strip()
    first_occurrence = firstOccurrence(text)
    count_table = countTable(text)
    patterns = lines[1].strip().split()
    for i in patterns:
        print bwtmatching_fast(text, i, first_occurrence, count_table),

    # suffixArray(text)
    # bwt(text)
    # print reconstruct(text)
    
