from numpy import *

# Logistic回归梯度上升优化算法
# ********************************************
'''
打开文件 testSet.txt，并逐行读取
'''


def loadDataSet():
    dataMat = [];
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        # 为方便计算将x0设为1.0
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


'''
梯度上升算法
dataMatIn:2维NumPy数组 (100x3)
classLabels:类标签 (1x100)
'''


def gradAscent(dataMatIn, classLabels):
    # 将输入转换为NumPy矩阵的数据类型（convert to NumPy matrix）
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()  # convert to NumPy matrix
    m, n = shape(dataMatrix)
    # 向目标移动的步长
    alpha = 0.001
    # 迭代次数
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):  # heavy on matrix operations
        h = sigmoid(dataMatrix * weights)  # matrix mult
        error = (labelMat - h)  # vector subtraction
        weights = weights + alpha * dataMatrix.transpose() * error  # matrix mult
    return weights


# ********************************************
'''
画出决策边界
'''


# 画出数据集和Logistic回归最佳拟合直线的函数
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = [];
    ycord1 = []
    xcord2 = [];
    ycord2 = []
    # 根据类别分别保存点
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]);
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1]);
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    # 最佳拟合线,此处设置了Sigmoid的z为0，因为0是两个分类的分界处
    # 即：0=w0x0+w1x1+w2x2
    # 注意：x0=1,x1=x,解出x2=y
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1');
    plt.ylabel('X2');
    plt.show()


# ********************************************
'''
改进的随机梯度上升算法
适用于数据集大，十亿或者成千上万
'''


# 注：最佳拟合直线并非最佳分类线
# 随机梯度上升算法基础版
def stocGradAscent0(dataMatrix, classLabels):
    m, n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)  # initialize to all ones
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights


# 改进的随机梯度上升算法
def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m, n = shape(dataMatrix)
    weights = ones(n)  # initialize to all ones
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.0001  # apha decreases with iteration, does not
            randIndex = int(random.uniform(0, len(dataIndex)))  # go to 0 because of the constant
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            # python3.x   range返回的是range对象，不返回数组对象
            del (list(dataIndex)[randIndex])
    return weights


if __name__ == '__main__':
    dataArr, labelMat = loadDataSet()
    print(gradAscent(dataArr, labelMat))
    weights = gradAscent(dataArr, labelMat)
    plotBestFit(weights.getA())
    weights = stocGradAscent0(array(dataArr), labelMat)
    plotBestFit(weights)
    weights = stocGradAscent1(array(dataArr), labelMat)
    plotBestFit(weights)
