import numpy as np

import matplotlib.pyplot as plt

# sklearn数据集 波士顿数据集
from sklearn.datasets import load_boston


def bostonMain():
    data, target = load_boston(return_X_y=True)
    print(data.shape)
    print(target.shape)


# 鸾尾花数据集
from sklearn.datasets import load_iris


def irisMain():
    iris = load_iris()
    print(iris.data.shape)
    print(iris.target.shape)
    print(list(iris.target_names))


# 手写数字数据集 包括1797个0-9的手写数字数据，每个数字由8*8大小的矩阵构成，矩阵中值的范围是0-16，代表颜色的深度
# n_class：表示返回数据的类别数；如n_class=5，则返回0-4的数据样本
from sklearn.datasets import load_digits


def digitsMain():
    digits = load_digits()
    plt.matshow(digits.images[0])
    plt.show
    print(digits.data.shape)
    print(digits.target.shape)
    print(digits.images.shape)
    # 图像的形式展示


if __name__ == '__main__':
    bostonMain()
    irisMain()
    digitsMain()
