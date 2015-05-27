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

def decoding(string, states, transition, emission):
    p = 1
    dic = {}

    dic[0] = {}
    for i in states:
        dic[0][i] = {}
        dic[0][i]['p'] = 1.0/len(states)*emission[(i,string[0])] 
    for i in xrange(1,len(string)):
        dic[i] = {}
        for j in states:
            dic[i][j] = {}
            max_value = -1
            pre_state = '' 
            for k in states:
                p_value = dic[i-1][k]['p']*transition[(k, j)]*emission[(j,string[i])]
                if p_value > max_value:
                    max_value = p_value
                    pre_state = k
            dic[i][j]['p'] = max_value
            dic[i][j]['pre_state'] = pre_state

    res = ''
    max_value = -1
    max_state = ''
    for i in states:
        if dic[len(string)-1][i]['p']>max_value:
            max_value = dic[len(string)-1][i]['p']
            max_state = i
    res = max_state+res
    for i in xrange(len(string)-1,0,-1):
        max_state = dic[i][max_state]['pre_state']
        res = max_state+res
    
    return res



def likelihood(string, states, transition, emission):
    p = 1
    dic = {}

    dic[0] = {}
    for i in states:
        dic[0][i] = {}
        dic[0][i] = 1.0/len(states)*emission[(i,string[0])] 
    for i in xrange(1,len(string)):
        dic[i] = {}
        for j in states:
            dic[i][j] = 0
            for k in states:
                dic[i][j] += dic[i-1][k]*transition[(k, j)]*emission[(j,string[i])]
    res = 0
    for i in states:
        res += dic[len(string)-1][i]
    return res
        

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


    # f = open('test', 'r')
    # lines = f.readlines()
    # string = lines[0].strip()
    # alphabet = lines[2].strip().split()
    # path = lines[4].strip()
    # states = lines[6].strip().split()
    # emission = {}
    # for i in xrange(9,9+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         emission[(states[i-9], alphabet[j-1])] = float(items[j])
    # res = emitt_prob(string, path, emission)
    # print res


    f = open('test', 'r')
    lines = f.readlines()
    string = lines[0].strip()
    alphabet = lines[2].strip().split()
    states = lines[4].strip().split()
    transition = {}
    for i in xrange(7,7+len(states)):
        items = lines[i].strip().split()
        for j in xrange(1,len(items)):
            transition[(states[i-7], states[j-1])] = float(items[j])

    emission = {}
    for i in xrange(11,11+len(states)):
        items = lines[i].strip().split()
        for j in xrange(1,len(items)):
            emission[(states[i-11], alphabet[j-1])] = float(items[j])


    # res = decoding(string, states, transition, emission)
    res = likelihood(string, states, transition, emission)
    print res


