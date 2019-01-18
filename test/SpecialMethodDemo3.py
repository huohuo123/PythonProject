# Python3中已经不能使用cmp()函数了，被如下五个函数替代:
import operator

# 意思是greater than（大于）
print(operator.gt(3, 2))
# 意思是greater and equal（大于等于）
print(operator.ge(3, 2))
# 意思是equal（等于）
print(operator.eq(3, 2))
# 意思是less and equal（小于等于）
print(operator.le(1, 2))
# #意思是less than（小于）
print(operator.lt(1, 2))
