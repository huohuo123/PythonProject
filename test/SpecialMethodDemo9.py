# python中 __slots__
# 由于Python是动态语言，任何实例在运行期都可以动态地添加属性。
# 如果要限制添加的属性，例如，Student类只允许添加 name、gender和score 这3个属性，就可以利用Python的一个特殊的__slots__来实现。
# 顾名思义，__slots__是指一个类允许的属性列表：


class Person(object):
    __slots__ = ('name', 'gender')

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    __slots__ = ('score',)

    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score


s = Student('Bob', 'male', 59)
s.name = 'Tim'
s.score = 99
print(s.score)
