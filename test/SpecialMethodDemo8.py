# python中 @property
# 第一个score(self)是get方法，用@property装饰，第二个score(self, score)是set方法，用@score.setter装饰，@score.setter是前一个@property装饰后的副产品。


class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score


s = Student('Python', 100)
s.score = 60
print(s.score)
