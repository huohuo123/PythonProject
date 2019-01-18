# python中数学运算1
# 表示有理数 p/q

class Rational(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q


class Rational(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __add__(self, r):
        return Rational(self.p * r.q + self.q * r.p, self.q * r.q)

    def __str__(self):
        return '%s/%s' % (self.p, self.q)

    __repr__ = __str__


r1 = Rational(1, 3)
r2 = Rational(1, 2)
print(r1)
print(r2)
print(r1+r2)
