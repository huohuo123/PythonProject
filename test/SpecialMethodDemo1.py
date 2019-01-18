# python中 __str__和__repr__
# 使用 __str__ 实现类到字符串的转化


class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score

    def __str__(self):
        return '(Student: %s, %s, %s)' % (self.name, self.gender, self.score)

    __repr__ = __str__


s = Student('Bob', 'male', 88)
print(s)
