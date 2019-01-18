# python中方法也是属性2

import types


def fn_get_grade(self):
    if self.score >= 80:
        return 'A'
    if self.score >= 60:
        return 'B'
    return 'C'


class Person(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score


p1 = Person('huo', 90)
p1.get_grade = types.MethodType(fn_get_grade, p1)
print(p1.get_grade())
