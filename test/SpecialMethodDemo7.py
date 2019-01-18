# python中类型转换
# Rational类实现了有理数运算，但是，如果要把结果转为 int 或 float 怎么办？

print(int(12.34))

print(float(12))

print(7 // 2)


class Rational(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __int__(self):
        return self.p // self.q


print(int(Rational(7, 2)))
print(int(Rational(1, 3)))
