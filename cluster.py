import sys, os, re

def FarthestFirstTraversal(data, k):
    start = data[0]
    centers = [start]
    data.remove(start)
    while len(centers)<k:
        max_value = 0
        max_point = []
        for i in data:
            distance = []
            for j in centers:
                tmp_distance = 0
                for n in xrange(len(i)):
                    tmp_distance += (i[n]-j[n])**2
                distance.append(tmp_distance)
            if min(distance)>max_value:
                max_value = min(distance)
                max_point = i
        centers.append(max_point)
        data.remove(max_point)
    return centers


if  __name__ == '__main__':
    f = open('test', 'r')
    lines = f.readlines()
    k = int(lines[0].split()[0])
    m = int(lines[0].split()[1])
    data = []
    for line in lines[1:]:
        data.append([float(x) for x in line.split()])
    res = FarthestFirstTraversal(data, k)

    for i in res:
        for j in i:
            print j,
        print

