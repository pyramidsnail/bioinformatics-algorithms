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


if __name__ == '__main__':
    lines = open('test', 'r').readlines()
    n = int(lines[0])
    dic = {}
    for line in lines[1:]:
        start = int(line.split('->')[0])
        end = int(line.split('->')[1].split(':')[0])
        weight = int(line.split('->')[1].split(':')[1])
        if start in dic:
            dic[start][end] = weight
        else:
            dic[start] = {}
            dic[start][end] = weight
    res = distanceMatrix(n, dic)

    for i in xrange(n):
        for j in xrange(n):
            print res[i][j],
        print
    
                
