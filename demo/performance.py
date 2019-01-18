import time
from functools import reduce
def performance(f):
       def fn(*args,**kw):
              t_start=time.time()
              r=f(*args,**kw)
              t_end=time.time()
              print('call %s() in %fs' %(f.__name__,(t_end-t_start)))
              return r
       return fn

@performance
def factorial(n):
       return reduce(lambda x,y:x*y,range(1,n+1))
print(factorial(10))
                                         
