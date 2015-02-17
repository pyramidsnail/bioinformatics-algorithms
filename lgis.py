f = open('test', 'rU')

n = int(f.readline())
seq = [int(x) for x in f.readline().split()]

 
arr = [1 for i in xrange(n)]
for i in xrange(1,n):
    for j in xrange(i):
        if seq[i]>seq[j] and arr[i]<arr[j]+1:
            arr[i] = arr[j]+1

index = arr.index(max(arr))
inc = [seq[index]]
for i in range(index, -1, -1):
    if arr[i] == arr[index]-1:
        inc.insert(0, seq[i])
        index = i
inc = [str(i) for i in inc]
print ' '.join(inc)


arr = [1 for i in xrange(n)]
for i in xrange(1,n):
    for j in xrange(i):
        if seq[i]<seq[j] and arr[i]<arr[j]+1:
            arr[i] = arr[j]+1

index = arr.index(max(arr))
dec = [seq[index]]
for i in range(index, -1, -1):
    if arr[i] == arr[index]-1:
        dec.insert(0, seq[i])
        index = i
dec = [str(i) for i in dec]
print ' '.join(dec)





#print ' '.join(arr)
    
# def lcs(seq, inc):
#     best = 0
#     opt = (0,0)
#     M = [[0 for i in xrange(len(inc)+1)] for i in xrange(len(seq)+1)]
#     for i in xrange(1,len(seq)+1):
#         for j in xrange(1,len(inc)+1):
#             M[i][j] = max(M[i-1][j-1]+[0,1]*[seq[i]==inc[j]], \
#                           M[i-1][j], M[i][j-1])
            
#             if M[i][j]>best:
#                 best = M[i][j]
#                 opt = 
