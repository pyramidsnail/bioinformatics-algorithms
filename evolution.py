import sys, os, re
import copy

def distanceMatrix(n, dic):
    res = copy.deepcopy(dic)
    flag = 0
    while flag == 0:
        for i in dic:
            for j in dic[i]:
                if j in dic:
                    for key in dic[j]:
                        if i in res:
                            if i == key:
                                 res[i][key] = 0
                            else:
                                if key in res[i]:
                                    res[i][key] = min((dic[i][j] + dic[j][key]), res[i][key])
                                else:
                                    res[i][key] = dic[i][j] + dic[j][key]

                        else:
                            res[i] = {}
                            if i == key:
                                res[i][key] = 0
                            else:
                                if key in res[i]:
                                    res[i][key] = min((dic[i][j] + dic[j][key]), res[i][key])
                                else:
                                     res[i][key] = dic[i][j] + dic[j][key]
        flag = 1
        for i in range(n):
            if not i in res:
                flag = 0
                break
            for j in range(n):
                if not j in res[i]:
                    flag = 0
                    break
        dic = copy.deepcopy(res) 
                    

    return res


def limbLength(n, dic):
    length = 1000000
    for i in xrange(len(dic)):
        for j in xrange(len(dic)):
            if i!=j and i!=n and j!=n:
                length = min((dic[i][n]+dic[j][n]-dic[i][j])/2, length)
    return length


def additivePhylogeny(dic, n, res):
    if n==2:
        if not dic.keys()[0] in res:
            res[dic.keys()[0]] = {}
        res[dic.keys()[0]][dic.keys()[1]] = dic[0][1]
        return res
    limblength = limbLength(len(dic)-1, dic)
    for i in xrange(len(dic)-1):
        dic[i][len(dic)-1] -= limblength
        dic[len(dic)-1][i] = dic[i][len(dic)-1]
    start = 0
    end = 0
    for i in xrange(len(dic)-1):
        for j in xrange(len(dic)-1):
            if i!=j and dic[i][j]==dic[i][len(dic)-1]+dic[j][len(dic)-1]:
                start = i
                end = j
    x = dic[start][len(dic)-1]
    #### add leaf
    
    dic.pop(len(dic)-1, None)
    return  additivePhylogeny(dic, n-1, res)
        
        



if __name__ == '__main__':

    ##### additivePhylogeny
    lines = open('test','r').readlines()
    n = int(lines[0])
    dic = {}
    for i in xrange(n):
        line = lines[i+1]
        items = line.split()
        dic[i] = {}
        for j in xrange(n):
            dic[i][j] = int(items[j])
    
    res = {}
    res = additivePhylogeny(dic, n, res)
    





    # ##### LimbLength
    # lines = open('test','r').readlines()
    # n = int(lines[1])
    # dic = {}
    # num = int(lines[0])
    # for i in xrange(num):
    #     line = lines[i+2]
    #     items = line.split()
    #     dic[i] = {}
    #     for j in xrange(num):
    #         dic[i][j] = int(items[j])

    # print limbLength(n, dic)

    # ##### build the distance Matrix
    # lines = open('test', 'r').readlines()
    # n = int(lines[0])
    # dic = {}
    # for line in lines[1:]:
    #     start = int(line.split('->')[0])
    #     end = int(line.split('->')[1].split(':')[0])
    #     weight = int(line.split('->')[1].split(':')[1])
    #     if start in dic:
    #         dic[start][end] = weight
    #     else:
    #         dic[start] = {}
    #         dic[start][end] = weight
    # res = distanceMatrix(n, dic)

    # for i in xrange(n):
    #     for j in xrange(n):
    #         print res[i][j],
    #     print
    
                
