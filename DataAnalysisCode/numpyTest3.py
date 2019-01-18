# 线性方程组和矩阵相关运算
# encoding=utf-8
import numpy as np
from numpy.linalg import *


def main():
    # 单位矩阵
    print(np.eye(3))
    # 加.表示浮点数
    lst = np.array([[1., 2.],
                    [3., 4.]])
    print("Inv:")
    # 逆矩阵
    print(inv(lst))
    # 转置矩阵
    print(lst.transpose())
    # 行列式
    print(det(lst))
    # 特征值和特征向量
    print(eig(lst))
    y = np.array([[5.], [7.]])
    # 求解方程组 x+2y=5 3x+6y=15
    print(solve(lst, y))


if __name__ == '__main__':
    main()
