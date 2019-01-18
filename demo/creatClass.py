class Person(object):
       address='Earth'
       def __init__(self,name):
              self.name=name

print(Person.address)
p1=Person('Bob')
p2=Person('Alice')
print(p1.address)
print(p2.address)
