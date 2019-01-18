# encoding=utf-8
import numpy as np


def main():
    # 常用操作
    # arange产生一个等差数列，范围1-11，不包含11
    print(np.arange(1, 11))
    # 多维数组
    print(np.arange(1, 11).reshape(2, -1))
    lst = np.arange(1, 11).reshape(2, -1)
    # 自然指数
    print(np.exp(lst))
    # 自然指数开方
    print(np.exp2(lst))
    print("Log:")
    # 自然数对数
    print(np.log(lst))

    # 对N个数组的操作

    lst = np.array([[[1, 2, 3, 4],
                     [4, 5, 6, 7]],
                    [[7, 8, 9, 10],
                     [10, 11, 12, 13]],
                    [[14, 15, 16, 17],
                     [18, 19, 20, 21]]])
    # axis常用的函数有：sum,max,min
    # 求和
    print(lst.sum())
    # axis最大值为维数-1
    # axis=0，表示只对最外层数组操作
    print(lst.sum(axis=0))
    # axis=1，表示再往里走一层
    print(lst.sum(axis=1))
    print(lst.sum(axis=2))
    # 把最大的值打印出来
    print(lst.max(axis=2))

    # 对两个数组的操作
    lst1 = np.array([10, 20, 30, 40])
    lst2 = np.array([4, 3, 2, 1])
    lst3 = np.array([8, 7, 6, 5])
    print("Add:")
    print(lst1 + lst2)
    print(lst1 - lst2)
    print(lst1 * lst2)
    print(lst1 / lst2)
    print(lst1 ** 2)
    # dot
    print("Dot:")
    # 点积计算
    print(np.dot(lst1.reshape([2, 2]), lst2.reshape([2, 2])))
    # 两个数组合并成一个集合
    print(np.concatenate((lst1, lst2), axis=0))
    # 可以实现n个数组合并
    print(np.concatenate((lst1, lst2, lst3), axis=0))
    # 合并，且换行
    # todo stack系列和concatenate的关系
    print(np.vstack((lst1, lst2)))
    print(np.hstack((lst1, lst2)))
    # 把数组1分成4份
    print(np.split(lst1, 4))
    # todo copy的深入理解
    print(np.copy(lst1))


if __name__ == '__main__':
    main()
