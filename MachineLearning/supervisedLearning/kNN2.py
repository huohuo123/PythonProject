# 使用kNN改进约会网站的配对效果
from numpy import *
import operator


# 创建已知数据信息
def createDataSet():
    group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def file2matrix(filename):
    """
     从文件中读入训练数据，并存储为矩阵
    """
    fr = open(filename)
    # get the number of lines in the file
    numberOfLines = len(fr.readlines())
    # 创建一个2维矩阵用于存放训练样本数据，一共有n行，每一行存放3个数据
    returnMat = zeros((numberOfLines, 3))
    # prepare labels return
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        # 把回车符号给去掉
        line = line.strip()
        # 把每一行数据用\t分割
        listFromLine = line.split('\t')
        # 把分割好的数据放至数据集，其中index是该样本数据的下标，就是放到第几行
        returnMat[index, :] = listFromLine[0:3]
        # 把该样本对应的标签放至标签集，顺序与样本集对应。
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector
