import sys, re, os

def fib(n,k):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n-1,k)+k*fib(n-2,k)

if __name__ =='__main__':
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    print fib(n,k)
