class Person(object):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


P1 = Person('Bob')
print(P1.get_name())
