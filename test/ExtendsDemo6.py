# python中获取对象信息
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score

    def whoAmI(self):
        return 'I am a Student, my name is %s' % self.name


print(type(123))
s = Student('Bob', 'Male', 88)
print(type(s))
# 可以用 dir() 函数获取变量的所有属性：
print(dir(123))
# dir()返回的属性是字符串列表，如果已知一个属性名称，要获取或者设置对象的属性，就需要用 getattr() 和 setattr( )函数了
print(getattr(s, 'name'))
setattr(s, 'name', 'huo')
print(s.name)
