import sys, os, re

def prob(path, transition):
    p = 0.5
    for i in xrange(len(path)-1):
        p *= transition[(path[i],path[i+1])]
    return p


def emitt_prob(string, path, emission):
    prob = 1
    for i in xrange(len(string)):
        prob *= emission[(path[i], string[i])]
    return prob 


if __name__ == '__main__':

    # f = open('test', 'r')
    # lines = f.readlines()
    # path = lines[0].strip()
    # states = lines[2].strip().split()
    # transition = {}
    # for i in xrange(5,5+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         transition[(states[i-5], states[j-1])] = float(items[j])
    # res = prob(path, transition)
    # print res


    f = open('test', 'r')
    lines = f.readlines()
    string = lines[0].strip()
    alphabet = lines[2].strip().split()
    path = lines[4].strip()
    states = lines[6].strip().split()
    emission = {}
    for i in xrange(9,9+len(states)):
        items = lines[i].strip().split()
        for j in xrange(1,len(items)):
            emission[(states[i-9], alphabet[j-1])] = float(items[j])
    res = emitt_prob(string, path, emission)
    print res


