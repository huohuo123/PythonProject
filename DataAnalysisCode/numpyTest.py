# encoding=utf-8
# numpy

import numpy as np


def main():
    lst = [[1, 3, 5], [2, 4, 6]]
    print(type(lst))
    np_lst = np.array(lst)
    print(type(np_lst))
    np_lst = np.array(lst, dtype=np.float)
    # 指定由两行，三列组成的
    print(np_lst.shape)
    # ndim维度，维数 2
    print(np_lst.ndim)
    # 数据类型
    print(np_lst.dtype)
    # 指定数据类型所占用字节
    print(np_lst.itemsize)
    # 大小
    print(np_lst.size)

    # some arrays
    print(np.zeros([2, 4]))
    print(np.ones([3, 5]))
    print("Rand:")
    print(np.random.rand(2, 4))
    print(np.random.rand())
    print("RandInt:")
    # 1-5中间的随机整数
    print(np.random.randint(1, 5))
    # 1-8中间的随机整数，连续生成3个
    print(np.random.randint(1, 8, 3))
    print("Random:")
    # 标准正太分布的随机数
    print(np.random.randn())
    # 标准正太分布的随机数,限定两行，4列
    print(np.random.randn(2, 4))
    # 指定范围的随机数
    print(np.random.choice([3, 2, 6, 4, 8]))
    print("Distribute:")
    # beta分布，1-10范围，100个
    print(np.random.beta(1, 10, 100))



    if __name__ == '__main__':
        main()
