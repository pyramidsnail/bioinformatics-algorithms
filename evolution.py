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
    #### determing whether this node exist
    # node_flag = 0
    # for i in dic[start]:
    #     if dic[start][i] == x:
    #             new_key = i
    #             node_flag = 1
    #             break
    # if not node_flag:
    new_key = max(res.keys()+dic.keys())+1
    if not new_key in res:
        res[new_key] = {}
    res[new_key][n-1] = limblength
    res[new_key][end] = dic[start][end]-x
    if not start in res:
        res[start] = {}
    res[start][new_key] = x

    dic.pop(len(dic)-1, None)
    for i in dic.keys():
        dic[i].pop(len(dic), None)
    return  additivePhylogeny(dic, n-1, res)

def additivePhylogeny1(dic, n)

def UPGMA(dic, n):
    graph = {}
    ncluster = n
    cluster_size = {}
    for i in xrange(n):
        cluster_size[i] = 1
    for i in xrange(n):
        graph[i] = {}
        graph[i]['age'] = 0
    while ncluster>1:
        min_value = 1000000
        point1 = 0
        point2 = 0
        for i in dic.keys():
            for j in dic.keys():
                if i!=j and dic[i][j] < min_value:
                    point1 = i
                    point2 = j
                    min_value = dic[i][j]
        new_key = len(graph)
        graph[new_key] = {}
        cluster_size[new_key] = cluster_size[point1] + cluster_size[point2]
        graph[new_key]['age'] = 1.0*(dic[point1][point2])/2
        graph[new_key][point1] = graph[new_key]['age'] - graph[point1]['age']
        graph[new_key][point2] = graph[new_key]['age'] - graph[point2]['age']
        dic[new_key] = {}
        for i in dic.keys():
            if i!=new_key:
                dic[new_key][i] = 1.0*(dic[point1][i]*cluster_size[point1]+dic[point2][i]*cluster_size[point2])/(cluster_size[point1]+cluster_size[point2])
                dic[i][new_key] = 1.0*(dic[point1][i]*cluster_size[point1]+dic[point2][i]*cluster_size[point2])/(cluster_size[point1]+cluster_size[point2])
        dic[new_key][new_key] = 0
        dic.pop(point1, None)
        dic.pop(point2, None)
        for i in dic.keys():
            dic[i].pop(point1, None)
            dic[i].pop(point2, None)
        ncluster -= 1          
        
    return graph

def neighborJoining(dic, n, graph):
    if n==2:
        if not dic.keys()[0] in graph:
            graph[dic.keys()[0]] = {}
        graph[dic.keys()[0]][dic.keys()[1]]=dic[dic.keys()[0]][dic.keys()[1]]
        return graph
    totalMatrix = {}
    for i in dic.keys():
        total = 0
        for j in dic[i].keys():
            if i!=j:
                total += dic[i][j]
        totalMatrix[i] = total
    neighborMatrix = {}
    for i in dic:
        if not i in neighborMatrix:
            neighborMatrix[i] = {}
        for j in dic[i]:
            if i==j:
                neighborMatrix[i][j] = 0
            else:
                neighborMatrix[i][j] = (n-2)*dic[i][j]-totalMatrix[i]-totalMatrix[j]

    min_value = 1000000
    point1 = 0
    point2 = 0
    for i in neighborMatrix:
        for j in neighborMatrix[i]:
            if neighborMatrix[i][j] < min_value:
                min_value = neighborMatrix[i][j]
                point1 = i
                point2 = j
    delta = 1.0*(totalMatrix[point1]-totalMatrix[point2])/(n-2)
    limb1 = 0.5*(dic[point1][point2]+delta)
    limb2 = 0.5*(dic[point1][point2]-delta)
    new_key = max(dic.keys())+1
    dic[new_key] = {}
    for i in dic:
        if i!=new_key:
            dic[new_key][i]=0.5*(dic[point1][i]+dic[point2][i]-dic[point1][point2])
            dic[i][new_key]=0.5*(dic[point1][i]+dic[point2][i]-dic[point1][point2])
    
    dic[new_key][new_key] = 0
    dic.pop(point1, None)
    dic.pop(point2, None)
    for i in dic.keys():
        dic[i].pop(point1, None)
        dic[i].pop(point2, None)

    if not new_key in graph:
        graph[new_key] = {}
    graph[new_key][point1] = limb1
    graph[new_key][point2] = limb2
    return neighborJoining(dic, n-1, graph)


def root_small_parsimony(graph, index):
    alphabet = ['A','T','C','G']
    tag = {}
    s = {}
    
    for i in graph:
        s[i] = {}
        if 'label' in graph[i] and len(graph[i]['label'])>=index:
            tag[i] = 1
            for symbol in alphabet:
                if i[index] == symbol:
                    s[i][symbol] = 0
                else:
                    s[i][symbol] = float('inf')
        else:
            tag[i] = 0

        for 
                    




if __name__ == '__main__':
    ##### rooted small parsimony
    f = open('test', 'r')
    graph = {}
    length = 0
    lines = f.readlines()
    n = int(lines[0])
    for line in lines[1:]:
        start = line.strip().split('->')[0]
        end = line.strip().split('->')[1]
        if len(end)>1:
            if graph.keys():
                new_key = max(graph.keys())+1
            else:
                new_key = 0
            length = len(end)
            graph[new_key] = {}
            graph[new_key]['label'] = end
        else:
            new_key = end
        if not start in graph:
            graph[start] = {}
        graph[start][new_key] = 0 
            
            
        
        


    

    # #####  neighbor joining
    # lines = open('test','r').readlines()
    # n = int(lines[0])
    # dic = {}
    # for i in xrange(n):
    #     line = lines[i+1]
    #     items = line.split()
    #     dic[i] = {}
    #     for j in xrange(n):
    #         dic[i][j] = int(items[j])
    # res ={}
    # res = neighborJoining(dic, n, res)
    # output = {}
    # for i in res:
    #     for j in res[i]:
    #         if j!='age':
    #             output[(i,j)] = res[i][j]
    #             output[(j,i)] = res[i][j]
    # for i in sorted(output.keys()):
    #     print "%s->%s:%.3f" %(i[0],i[1],output[(i[0],i[1])])






    # #####  UPGMA
    # lines = open('test','r').readlines()
    # n = int(lines[0])
    # dic = {}
    # for i in xrange(n):
    #     line = lines[i+1]
    #     items = line.split()
    #     dic[i] = {}
    #     for j in xrange(n):
    #         dic[i][j] = int(items[j])
    # res =UPGMA(dic, n)
    # output = {}
    # for i in res:
    #     for j in res[i]:
    #         if j!='age':
    #             output[(i,j)] = res[i][j]
    #             output[(j,i)] = res[i][j]
    # for i in sorted(output.keys()):
    #     print "%s->%s:%.3f" %(i[0],i[1],output[(i[0],i[1])])

    # ##### additivePhylogeny
    # lines = open('test','r').readlines()
    # n = int(lines[0])
    # dic = {}
    # for i in xrange(n):
    #     line = lines[i+1]
    #     items = line.split()
    #     dic[i] = {}
    #     for j in xrange(n):
    #         dic[i][j] = int(items[j])
    
    # res = {}
    # res = additivePhylogeny(dic, n, res)
    





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
    
                
