from functools import reduce
def f(x,y):
       return x+y

print(reduce(f,[1,3,5,7,9],100))
