# python中方法也是属性
class Person(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        return 'A'


p1 = Person('huo', 90)
print(p1.get_grade())
