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

# def additivePhylogeny1(dic, n)

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
    res = {}
    alphabet = ['A','T','C','G']
    tag = {}
    s = {}
    track_table = {}
    for i in graph:
        s[i] = {}
        track_table[i] = {}
        if 'label' in graph[i] and len(graph[i]['label'])>=index:
            tag[i] = 1
            res[i] = graph[i]['label'][index]
            track_table[i] = {}
            track_table[i][graph[i]['label'][index]] = '$' 
            for symbol in alphabet:
                if graph[i]['label'][index] == symbol:
                    s[i][symbol] = 0
                else:
                    s[i][symbol] = float('inf')
        else:
            tag[i] = 0

    while 0 in tag.values():
        for i in graph: 
            if tag[i]==0:
                flag = 1
                for k in graph[i]:
                    if len(s[k])!=4:
                        flag = 0
                if flag:
                    tag[i] = 1
                    track_table[i] = {}
                    for symbol in alphabet:
                        s[i][symbol] = 0
                        track_table[i][symbol] = {}
                        for k in xrange(len(graph[i])):
                            if k!='label':
                                min_value = 1000000
                                for sub_symbol in alphabet:
                                    if symbol == sub_symbol:
                                        if s[graph[i].keys()[k]][sub_symbol] < min_value:
                                            min_value = s[graph[i].keys()[k]][sub_symbol]
                                            track_table[i][symbol][k] = sub_symbol
                                    
                                    else:
                                        if (s[graph[i].keys()[k]][sub_symbol]+1) < min_value:
                                            min_value = s[graph[i].keys()[k]][sub_symbol]+1
                                            track_table[i][symbol][k] = sub_symbol
                                        
                            s[i][symbol] += min_value
    
    
    top_node = max(graph.keys())
    res[top_node] = min(s[i], key=s[i].get)
    # search_node = top_node
    # while len(track_table[search_node])==4:
    #     for k in graph[search_node]:
    #         res[k] = track_table[search_node][res[search_node]]
    queue = []
    queue.append(top_node)
    while queue:
        item = queue.pop()
        son = graph[item].keys()[0]
        daughter = graph[item].keys()[1]
        res[son] = track_table[item][res[item]][0]
        res[daughter] = track_table[item][res[item]][1]
        if len(graph[son])>1:
            queue.append(son)
        if len(graph[daughter])>1:
            queue.append(daughter)
   
    
        
    return [res, min(s[top_node].values())]



def hamming(str1, str2):
    score = 0
    for i in xrange(len(str1)):
        if str1[i]!=str2[i]:
            score += 1
    return score


def nearest_neighbor(graph, node1, node2):
    neighbors = [copy.deepcopy(graph), copy.deepcopy(graph)]
#     neighbor2 = copy.deepcopy(graph)
    for i in graph[node1]:
        if i!=node2:
            node1_exchange = i
            break
    node2_exchange = []
    for i in graph[node2]:
        if i!=node1:
            node2_exchange.append(i)
    for i in xrange(2):
        neighbors[i][node1][graph[node1].index(node1_exchange)] = node2_exchange[i]
        neighbors[i][node2][graph[node2].index(node2_exchange[i])] = node1_exchange
        neighbors[i][node1_exchange][graph[node1_exchange].index(node1)] = node2
        neighbors[i][node2_exchange[i]][graph[node2_exchange[i]].index(node2)] = node1
    return neighbors


        
def small_parsimony_params(graph):
    min_res = {}
    min_score = 1000000
    final_graph = {}
    final_node = 0
    final_sub_node = 0
    final_add_key = 0
    for node in graph:
        if  'label' not in graph[node] and len(graph[node])==3:
            for sub_node in graph[node]:
                if 'label' not in graph[sub_node]:
                    tmp_graph = copy.deepcopy(graph)
                    add_key = max(tmp_graph.keys())+1
                    tmp_graph[add_key] = {}
                    tmp_graph[add_key][node] = 0
                    tmp_graph[add_key][sub_node] = 0
                    tmp_graph[node].pop(sub_node, None)
                    score = 0
                    res = {}
                    for i in tmp_graph.keys():
                        res[i] = ''
                    for i in xrange(length):
                        tmp, tmp_score = root_small_parsimony(tmp_graph, i)
                        score += tmp_score
                        for j in tmp_graph.keys():
                            res[j] += tmp[j]
                    if score<min_score:
                        min_score = score
                        min_res = copy.deepcopy(res)
                        final_graph = copy.deepcopy(tmp_graph)
                        final_node = node
                        final_sub_node = sub_node
                        final_add_key = add_key
                    # graph.pop(max(graph.keys())+1, None)
                        final_graph.pop(final_add_key, None)

    return [min_score, final_graph, final_add_key, min_res, final_node, final_sub_node]

def pprint(final_graph, final_add_key,min_res, final_node, final_sub_node):
    # print min_score
    for key in final_graph:
        if 'label' not in final_graph[key]:
            for sub_key in final_graph[key]:
                print "%s->%s:%d" %(min_res[key],min_res[sub_key],hamming(min_res[key], min_res[sub_key]))
                print "%s->%s:%d" %(min_res[sub_key], min_res[key], hamming(min_res[key], min_res[sub_key]))
    print "%s->%s:%d" %(min_res[final_node],min_res[final_sub_node],hamming(min_res[final_node], min_res[final_sub_node]))
    print "%s->%s:%d" %(min_res[final_sub_node],min_res[final_node],hamming(min_res[final_node], min_res[final_sub_node]))

    

if __name__ == '__main__':


    ##### large parsimony
    f = open('test', 'r')
    graph = {}
    length = 0
    lines = f.readlines()
    org_key = -1
    n = int(lines[0])
    for i in xrange(len(lines)-1):
        start = lines[i+1].strip().split('->')[0]
        end = lines[i+1].strip().split('->')[1]
        if str.isdigit(start):
            if not str.isdigit(end):
                length = len(end)
                new_key = org_key+1
                org_key = new_key
                graph[new_key] = {}
                graph[new_key]['label'] = end
            else:
                new_key = int(end)
            if int(start) > new_key:
                if not int(start) in graph:
                    graph[int(start)] = {}
                graph[int(start)][new_key] = 0
            # if not int(start) in graph:
            #     graph[int(start)] = {}
            # if not new_key in graph:
            #     graph[int(start)][new_key] = 0
            # else:
            #     if (not int(start) in graph[new_key]):
            #         graph[int(start)][new_key] = 0
    neighbor_min_score = small_parsimony_params(graph)[0]
    ### loop through all the internal edges
    ### determine node1 and node2
    #### multiple choices
    rerun_update_graph = 1

    while rerun_update_graph:
        rerun_update_graph = 0
        node_set = {}
        for node in graph:
            if  'label' not in graph[node]:
                for sub_node in graph[node]:
                    if 'label' not in graph[sub_node]:
                        if not node in node_set:
                            node_set[node] = [] 
                        node_set[node].append(sub_node)
      ### interchange neighbors
        node1 = node_set.keys()[0]
        node2 = node_set[node1][len(node_set[node1])-1]
        rm_node_set = []
        while True:
            ### update looped edges
            update_graph = 0
            rm_key = []
            for key in node_set:
                if not node_set[key]:
                    rm_key.append(key)
            for key in rm_key:
                node_set.pop(key, None)
            if not node_set:
                break

            node1 = node_set.keys()[0]
            node2 = node_set[node1][0]
            large_parsimony_graph = {}
            for i in graph:
                large_parsimony_graph[i] = []
            for i in graph:
                for j in graph[i]:
                    if len(graph[i])>1:
                        large_parsimony_graph[i].append(j)
                        large_parsimony_graph[j].append(i)
            neighbors = nearest_neighbor(large_parsimony_graph, node1, node2)
            ### transform neighbors into unrooted small parsimony input
            for neighbor in neighbors:
                # update_graph = 0
                # neighbor_min_score = large_parsimony_min
                small_parsimony_graph = {}
                for i in graph:
                    if 'label' in graph[i]:
                        small_parsimony_graph[i] = {}
                        small_parsimony_graph[i]['label'] = graph[i]['label']
                    else:
                        small_parsimony_graph[i] = {}
                        count_ripe = 0
                        for j in neighbor[i]:
                            if j in small_parsimony_graph and len(small_parsimony_graph[j])>0:
                                count_ripe += 1
                        if count_ripe >1:
                            for j in neighbor[i]:
                                 if   j in small_parsimony_graph and len(small_parsimony_graph[j])>0:
                                     small_parsimony_graph[i][j] = 0
                full_dict = 0
                while not full_dict:
                    full_dict_count = 0
                    for i in small_parsimony_graph:
                        if not small_parsimony_graph[i]:
                            full_dict_count += 1
                            count_ripe = 0
                            for j in neighbor[i]:
                                if j in small_parsimony_graph and len(small_parsimony_graph[j])>0:
                                    count_ripe += 1
                            if count_ripe >1:
                                for j in neighbor[i]:
                                    if   j in small_parsimony_graph and len(small_parsimony_graph[j])>0:
                                        small_parsimony_graph[i][j] = 0
                    if full_dict_count == 0:
                        full_dict =1



                            # # if i>j  and (i not in small_parsimony_graph[j]):
                            # #      small_parsimony_graph[i][j] = 0
                            # if j not in small_parsimony_graph:
                            #     small_parsimony_graph[i][j] = 0
                            # else:
                            #     if i not in small_parsimony_graph[j]:
                            #         small_parsimony_graph[i][j] = 0

                min_res = {}
                min_score = 1000000
                final_small_parsimony_graph = {}
                final_node = 0
                final_sub_node = 0
                final_add_key = 0
                for node in small_parsimony_graph:
                    if  'label' not in small_parsimony_graph[node] and len(small_parsimony_graph[node])==3:
                        for sub_node in small_parsimony_graph[node]:
                            if 'label' not in small_parsimony_graph[sub_node]:
                                tmp_small_parsimony_graph = copy.deepcopy(small_parsimony_graph)
                                add_key = max(tmp_small_parsimony_graph.keys())+1
                                tmp_small_parsimony_graph[add_key] = {}
                                tmp_small_parsimony_graph[add_key][node] = 0
                                tmp_small_parsimony_graph[add_key][sub_node] = 0
                                tmp_small_parsimony_graph[node].pop(sub_node, None)
                                score = 0
                                res = {}
                                for i in tmp_small_parsimony_graph.keys():
                                    res[i] = ''
                                for i in xrange(length):
                                    tmp, tmp_score = root_small_parsimony(tmp_small_parsimony_graph, i)
                                    score += tmp_score
                                    for j in tmp_small_parsimony_graph.keys():
                                        res[j] += tmp[j]
                                if score<min_score:
                                    min_score = score
                                    min_res = copy.deepcopy(res)
                                    final_small_parsimony_graph = copy.deepcopy(tmp_small_parsimony_graph)
                                    final_node = node
                                    final_sub_node = sub_node
                                    final_add_key = add_key
                                # # small_parsimony_graph.pop(max(small_parsimony_graph.keys())+1, None)

                if min_score<neighbor_min_score:
                    neighbor_min_score = min_score
                    update_graph = 1
                    rerun_update_graph = 1
                    final_small_parsimony_graph.pop(final_add_key, None)
                    graph = copy.deepcopy(final_small_parsimony_graph)
                    graph[final_node][final_sub_node] = 0


                    output_final_node = final_node
                    output_final_sub_node = final_sub_node
                    output_min_res = min_res
            if update_graph:
                print 
                print neighbor_min_score
                # final_small_parsimony_graph.pop(final_add_key, None)
                for key in graph:
                    if 'label' not in graph[key]:
                        for sub_key in graph[key]:
                            print "%s->%s:%d" %(output_min_res[key],output_min_res[sub_key],hamming(output_min_res[key], output_min_res[sub_key]))
                            print "%s->%s:%d" %(output_min_res[sub_key], output_min_res[key], hamming(output_min_res[key], output_min_res[sub_key]))
                print "%s->%s:%d" %(output_min_res[output_final_node],output_min_res[output_final_sub_node],hamming(output_min_res[output_final_node], output_min_res[output_final_sub_node]))
                print "%s->%s:%d" %(output_min_res[output_final_sub_node],output_min_res[output_final_node],hamming(output_min_res[output_final_node], output_min_res[output_final_sub_node]))


            node_set[node1].remove(node2)
            rm_node_set.append((node1, node2))
            if node1 in node_set:
                for i in node_set[node1]:
                    if i not in graph[node1]:
                        if not node2 in node_set:
                            node_set[node2] = []
                        if i not in  node_set[node2] and (i,node2) not in rm_node_set and (node2, i) not in rm_node_set:
                            node_set[node2].append(i)
                        node_set[node1].remove(i)
            if 'label' not in graph[node2]:
                for sub_node in graph[node2]:
                    if 'label' not in graph[sub_node]:
                        if not node2 in node_set:
                            node_set[node2] = []
                        if sub_node not in  node_set[node2] and (sub_node,node2) not in rm_node_set and (node2, sub_node) not in rm_node_set:
                            node_set[node2].append(sub_node)

            if node2 in node_set:
                for i in node_set[node2]:
                    if i not in graph[node2]:
                        if not node1 in node_set:
                            node_set[node1] = []
                        if i not in  node_set[node1] and (i,node1) not in rm_node_set and (node1, i) not in rm_node_set:
                            node_set[node1].append(i) 
                        node_set[node2].remove(i)

            if 'label' not in graph[node1]:
                for sub_node in graph[node1]:
                    if 'label' not in graph[sub_node]:
                        if not node1 in node_set:
                            node_set[node1] = []
                        if sub_node not in  node_set[node1] and (sub_node,node1) not in rm_node_set and (node1, sub_node) not in rm_node_set:
                            node_set[node1].append(sub_node)



                # print min_score
                # final_small_parsimony_graph.pop(final_add_key, None)
                # for key in final_small_parsimony_graph:
                #     if 'label' not in final_small_parsimony_graph[key]:
                #         for sub_key in final_small_parsimony_graph[key]:
                #             print "%s->%s:%d" %(min_res[key],min_res[sub_key],hamming(min_res[key], min_res[sub_key]))
                #             print "%s->%s:%d" %(min_res[sub_key], min_res[key], hamming(min_res[key], min_res[sub_key]))
                # print "%s->%s:%d" %(min_res[final_node],min_res[final_sub_node],hamming(min_res[final_node], min_res[final_sub_node]))
                # print "%s->%s:%d" %(min_res[final_sub_node],min_res[final_node],hamming(min_res[final_node], min_res[final_sub_node]))


                






                    
   # ##### nearest neighbors
   #  f = open('test', 'r')
   #  lines = f.readlines()
   #  graph = {}
   #  node1 = int(lines[0].split()[0])
   #  node2 = int(lines[0].strip().split()[1])
   #  for line in lines[1:]:
   #      start = int(line.split('->')[0])
   #      end = int(line.strip().split('->')[1])
   #      if not start in graph:
   #          graph[start] = []
   #      graph[start].append(end)

   #  neighbors = nearest_neighbor(graph, node1, node2)
   #  for i in neighbors:
   #      for j in i:
   #          for k in i[j]:
   #              print "%s->%s" %(j,k)
   #      print 
    

    # ##### unrooted small parsimony
    # f = open('test', 'r')
    # graph = {}
    # length = 0
    # lines = f.readlines()
    # n = int(lines[0])
    # for i in xrange(len(lines)-1):
    #     if (i+1)%2==0:
    #         start = int(lines[i+1].strip().split('->')[0])
    #         end = lines[i+1].strip().split('->')[1]
    #         if not str.isdigit(end):
    #             length = len(end)
    #             new_key = (i+1)/2-1
    #             graph[new_key] = {}
    #             graph[new_key]['label'] = end
    #         else:
    #             new_key = int(end)
    #         if not start in graph:
    #             graph[start] = {}
    #         graph[start][new_key] = 0 
 

    # min_res = {}
    # min_score = 1000000
    # final_graph = {}
    # final_node = 0
    # final_sub_node = 0
    # final_add_key = 0
    # for node in graph:
    #     if  'label' not in graph[node] and len(graph[node])==3:
    #         for sub_node in graph[node]:
    #             if 'label' not in graph[sub_node]:
    #                 tmp_graph = copy.deepcopy(graph)
    #                 add_key = max(tmp_graph.keys())+1
    #                 tmp_graph[add_key] = {}
    #                 tmp_graph[add_key][node] = 0
    #                 tmp_graph[add_key][sub_node] = 0
    #                 tmp_graph[node].pop(sub_node, None)
    #                 score = 0
    #                 res = {}
    #                 for i in tmp_graph.keys():
    #                     res[i] = ''
    #                 for i in xrange(length):
    #                     tmp, tmp_score = root_small_parsimony(tmp_graph, i)
    #                     score += tmp_score
    #                     for j in tmp_graph.keys():
    #                         res[j] += tmp[j]
    #                 if score<min_score:
    #                     min_score = score
    #                     min_res = copy.deepcopy(res)
    #                     final_graph = copy.deepcopy(tmp_graph)
    #                     final_node = node
    #                     final_sub_node = sub_node
    #                     final_add_key = add_key
    #                 # graph.pop(max(graph.keys())+1, None)
    
    # print min_score
    # final_graph.pop(final_add_key, None)
    # for key in final_graph:
    #     if 'label' not in final_graph[key]:
    #         for sub_key in final_graph[key]:
    #             print "%s->%s:%d" %(min_res[key],min_res[sub_key],hamming(min_res[key], min_res[sub_key]))
    #             print "%s->%s:%d" %(min_res[sub_key], min_res[key], hamming(min_res[key], min_res[sub_key]))
    # print "%s->%s:%d" %(min_res[final_node],min_res[final_sub_node],hamming(min_res[final_node], min_res[final_sub_node]))
    # print "%s->%s:%d" %(min_res[final_sub_node],min_res[final_node],hamming(min_res[final_node], min_res[final_sub_node]))
    
    
    # ##### rooted small parsimony
    # f = open('test', 'r')
    # graph = {}
    # length = 0
    # lines = f.readlines()
    # n = int(lines[0])
    # for i in xrange(len(lines)-1):
    #     start = int(lines[i+1].strip().split('->')[0])
    #     end = lines[i+1].strip().split('->')[1]
    #     if not str.isdigit(end):
    #         length = len(end)
    #         new_key = i
    #         graph[new_key] = {}
    #         graph[new_key]['label'] = end
    #     else:
    #         new_key = int(end)
    #     if not start in graph:
    #         graph[start] = {}
    #     graph[start][new_key] = 0 

    # # res = root_small_parsimony(graph, 2)
    

    # res = {}
    # score = 0

    # for i in graph.keys():
    #     res[i] = ''
    # for i in xrange(length):
    #     tmp, tmp_score = root_small_parsimony(graph, i)
    #     score += tmp_score
    #     for j in graph.keys():
    #         res[j] += tmp[j]

    # for key in graph:
    #     if 'label' not in graph[key]:
    #         for sub_key in graph[key]:
    #             print "%s->%s:%d" %(res[key],res[sub_key],hamming(res[key], res[sub_key]))
    #             print "%s->%s:%d" %(res[sub_key], res[key], hamming(res[key], res[sub_key]))
    # print score        
            

    
        
        


    

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
    
                
