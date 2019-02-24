# 实现需求：有以下先验数据，使用knn算法对未知类别数据分类。
# 就和看电影的场景是一样的。电影有两个属性A:打斗镜头 B：接吻镜头 已知电影1，2，3，4的电影类型，求未知类型到底是动作片还是爱情片
from numpy import *
import operator

# 创建已知数据信息
def createDataSet():
    group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    """
 21 inX 是输入的测试样本，是一个[x, y]样式的
 22 dataset 是训练样本集
 2  labels 是训练样本标签
 2  k 是top k最相近的
 2  """
    # shape返回矩阵的[行数，列数]，
    # 那么shape[0]获取数据集的行数，
    # 行数就是样本的数量
    dataSetSize = dataSet.shape[0]
    # tile属于numpy模块下边的函数
    # tile（A, reps）返回一个shape=reps的矩阵，矩阵的每个元素是A;reps则决定A重复的次数
    # 比如 A=[0,1,2] 那么，tile(A, 2)= [0, 1, 2, 0, 1, 2]
    # 这个地方就是为了把输入的测试样本扩展为和dataset的shape一样，然后就可以直接做矩阵减法了。
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    # diffMat是一个矩阵，矩阵**2表示对矩阵中的每个元素进行**2操作，即平方。
    sqDiffMat = diffMat ** 2
    # axis=1表示按照横轴，sum表示累加，即按照行进行累加。
    # sqDistance = [[1.01],
    #               [1.0 ],
    #               [1.0 ],
    #               [0.81]]
    sqDistances = sqDiffMat.sum(axis=1)
    # 对平方和进行开根号
    distances = sqDistances ** 0.5
    # 按照升序进行快速排序，返回的是原数组的下标。
    # 比如，x = [30, 10, 20, 40]
    # 升序排序后应该是[10,20,30,40],他们的原下标是[1,2,0,3]
    # 那么，numpy.argsort(x) = [1, 2, 0, 3]
    sortedDistIndicies = distances.argsort()
    # 存放最终的分类结果及相应的结果投票数
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


if __name__ == '__main__':
    dateSet, labels = createDataSet()
    inX = [1.2, 1.0]
    inY = [0.1, 0.3]
    className = classify0(inX, dateSet, labels, 3)
    className2 = classify0(inY, dateSet, labels, 3)
    print(className)
    print(className2)
