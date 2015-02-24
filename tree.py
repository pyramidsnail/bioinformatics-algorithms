import sys, re, os

f = open('test','rU')
lines = f.readlines()
n = int(lines[0].strip())
parent={}
for i in xrange(1,n+1):
    parent[i] = i

def union(u,v):
    r1 = find(u)
    r2 = find(v)
    parent[r2] = r1



def find(u):
    while parent[u] != u:
        u = parent[u]
    return u

for i in lines[1:]:
    start = int(i.strip().split()[0])
    end = int(i.strip().split()[1])
    union(start, end)


count = 0
for i in parent:
    if i == parent[i]:
        count += 1
print count-1



# contain = []
# parts = []
# for i in lines[1:]:
#     start = i.strip().split()[0]
#     end = i.strip().split()[1]
#     if not start in contain:
#         contain.append(start)
#     if not end in contain:
#         contain.append(end)
#     flag = 0
#     for x in parts:
#         if start in x or end in x:
#             x.extend([start, end])
#             flag = 1
#             break
#     if not flag:
#         parts.append([start, end])



# print int(lines[0].strip())-len(contain)+len(parts)-1
    
