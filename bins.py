import sys, os, re

def bins(start, num, array):
    if num > array[len(array)/2] and num <= array[-1]:
        return bins(start+len(array)/2, num, array[len(array)/2:])
    elif num < array[len(array)/2]and num >= array[0]:
        return bins(start, num, array[:len(array)/2])
    elif num == array[len(array)/2]:
        return start+len(array)/2
    else:
        return -1

if __name__ == '__main__':
    f = open('rosalind_bins.txt','r')
    lines = f.readlines()
    array = lines[2].strip().split()
    array = [int(x) for x in array]
    nums =  lines[3].strip().split()
    nums = [int(x) for x in nums]
    for i in nums:
        print bins(1, i, array),
