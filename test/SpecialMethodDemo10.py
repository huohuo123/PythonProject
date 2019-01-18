# 所有的函数都是可调用对象。
# 一个类实例也可以变成一个可调用对象，只需要实现一个特殊方法__call__()。
# 斐波那契数列


class Fib(object):
    def __call__(self, num):
        a, b, L = 0, 1, []
        for n in range(num):
            L.append(a)
            a, b = b, a + b
        return L


f = Fib()
print(f(10))
