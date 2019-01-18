# python中判断类型
# 函数isinstance()可以判断一个变量的类型，既可以用在Python内置的数据类型如str、list、dict，也可以用在我们自定义的类，它们本质上都是数据类型。

class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score


class Teather(Person):
    def __init__(self, name, gender, course):
        super(Teather, self).__init__(name, gender)
        self.course = course


p = Person('Bob', 12)
s = Student('huo', 18, 90)
t = Teather('mi', 44, 'English')

print(s.gender)

# 在继承链上，一个父类的实例不能是子类类型，因为子类比父类多了一些属性和方法
print(isinstance(p, Person))
print(isinstance(p, Student))
print(isinstance(p, Teather))

# 一条继承链上，一个实例可以看成它本身的类型，也可以看成它父类的类型。
print(isinstance(s, Person))
print(isinstance(s, Student))
print(isinstance(s, Teather))
