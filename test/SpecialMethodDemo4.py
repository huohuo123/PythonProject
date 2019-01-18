# python中 __len__
# 如果一个类表现得像一个list，要获取有多少个元素，就得用 len() 函数。


class Students(object):
    def __init__(self, *args):
        self.names = args

    def __len__(self):
        return len(self.names)


ss = Students('Bob', 'Alice', 'Tim')
print(len(ss))
