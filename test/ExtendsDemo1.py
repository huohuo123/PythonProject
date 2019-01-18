# python中继承一个类
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score


t = Student('huo', 12, 60)
print(t.name)
print(t.gender)
