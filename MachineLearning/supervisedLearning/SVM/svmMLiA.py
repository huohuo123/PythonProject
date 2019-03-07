from numpy import *
from time import sleep

# ****************************************************
# 可以看出，这里采用的类别标签是-1，1，而不是0和1
'''
打开文件，并对其逐行解析，从而得到每行的类标签和整个数据矩阵
'''


def loadDataSet(fileName):
    dataMat = [];
    labelMat = [];
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat


'''
i是第一个alpha的下标；m是所有alpha的数目
只要函数值不等于输入值i，函数就会进行随机选择
'''


def selectJrand(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j


'''
用于调整大于H或小于L的alpha值。
'''


def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj


# ****************************************************
# SMO算法的第一版本
# 伪代码如下
'''
创建一个alpha向量并将其初始化为0向量
当迭代次数小于最大迭代次数时（外循环）
    对数据集中的每个数据向量（内循环）：
如果该数据向量可以被优化：
    随机选择另外一个数据向量
    同时优化这两个向量
    如果两个向量都不能被优化，退出内循环
'''

'''
dataMatIn:数据集
classLabels:类别标签
C:常数C
toler:容错率
maxIter:退出前最大的循环次数
本方法将多个列表和输入参数转换成NumPy矩阵，简化了很多数学处理操作

'''


def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn);
    labelMat = mat(classLabels).transpose()
    b = 0;
    m, n = shape(dataMatrix)
    alphas = mat(zeros((m, 1)))
    iter = 0
    while (iter < maxIter):
        # alphaPairsChanged用于记录alpha是否已经进行优化
        alphaPairsChanged = 0
        # 遍历整个集合
        for i in range(m):
            fXi = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fXi - float(labelMat[i])
            # if((labelMat[i]*Ei<-toler) and (alphas[i]<c)) or \((labelMat[i]*Ei)>toler) and \(alphas[i]>0)):
            if ((labelMat[i] * Ei < -toler) and (alphas[i] < C)) or ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i, m)
            fXj = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[j, :].T)) + b
            Ej = fXj - float(labelMat[j])
            alphaIold = alphas[i].copy();
            alphaJold = alphas[j].copy();
        if (labelMat[i] != labelMat[j]):
            L = max(0, alphas[j] - alphas[i])
            H = min(C, C + alphas[j] - alphas[i])
        else:
            L = max(0, alphas[j] + alphas[i] - C)
            H = min(C, alphas[j] + alphas[i])
        if L == H: print("L==H"); continue
        eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - dataMatrix[i, :] * dataMatrix[i, :].T - dataMatrix[j,
                                                                                                    :] * dataMatrix[j,
                                                                                                         :].T
        if eta >= 0: print("eta>=0"); continue
        alphas[j] -= labelMat[j] * (Ei - Ej) / eta
        alphas[j] = clipAlpha(alphas[j], H, L)
        if (abs(alphas[j] - alphaJold) < 0.00001): print("j not moving enough"); continue
        alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])  # update i by the same amount as j
        # the update is in the oppostie direction
        b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T - labelMat[j] * (
                alphas[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T
        b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T - labelMat[j] * (
                alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T
        if (0 < alphas[i]) and (C > alphas[i]):
            b = b1
        elif (0 < alphas[j]) and (C > alphas[j]):
            b = b2
        else:
            b = (b1 + b2) / 2.0
        alphaPairsChanged += 1
        print("iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged))
    if (alphaPairsChanged == 0):
        iter += 1
    else:
        iter = 0
    print("iteration number: %d" % iter)
    return b, alphas


# ****************************************************
# 完整版Platt SMO的支持函数
# todo 未懂，暂时放下 2019年03月07日10:37:39


if __name__ == '__main__':
    dataArr, labelArr = loadDataSet('testSet.txt')
    # print(labelArr)
    b, alphas = smoSimple(dataArr, labelArr, 0.6, 0.001, 40)
    # todo 不晓得输出结果什么意思？  2019年03月07日10:29:53
    # ************************************
    # print(b,alphas)
    shape(alphas[alphas > 0])
    for i in range(100):
        if alphas[i] > 0.0:
            print(dataArr[i], labelArr[i])
    # ************************************
