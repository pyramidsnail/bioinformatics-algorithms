k, m, n = [int(x) for x in raw_input().split()]
total = k+m+n

stats = 1.0/(total*(total-1))*(k**2-k+2*k*m+0.75*m**2-0.75*m+2*k*n+m*n)
print stats
