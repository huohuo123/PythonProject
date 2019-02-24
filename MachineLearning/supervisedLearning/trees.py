# 决策树的构造
from math import log
import operator


def calc_shannon_ent(data_set):
    num_entries = len(data_set)
    label_counts = {}
    # 统计每个类别出现的次数，保存在字典labelCounts中
    for featVec in data_set:
        current_label = featVec[-1]
        if current_label not in label_counts.keys(): label_counts[current_label] = 0
        # 如果当前键值不存在，则扩展字典并将当前键值加入字典
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        # 使用所有类标签的发生频率计算类别出现的概率
        prob = float(label_counts[key]) / num_entries
        # 用这个概率计算香农熵 ,取2为底的对数
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def create_data_set():
    data_set = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    # change to discrete values
    return data_set, labels


'''
按照给定特征划分数据集
dataSet：待划分的数据集
axis：   划分数据集的第axis个特征
value：  特征的返回值（比较值）
'''


def split_data_set(dataSet, axis, value):
    ret_data_set = []
    # 遍历数据集中的每个元素，一旦发现符合要求的值，则将其添加到新创建的列表中
    for featVec in dataSet:
        if featVec[axis] == value:
            reduced_feat_vec = featVec[:axis]  # chop out axis used for splitting
            reduced_feat_vec.extend(featVec[axis + 1:])
            # extend()和append()方法功能相似，但在处理列表时，处理结果完全不同
            # a=[1,2,3]  b=[4,5,6]
            # a.append(b) = [1,2,3,[4,5,6]]
            # a.extend(b) = [1,2,3,4,5,6]
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set


'''
选择最好的数据集划分方式
输入：数据集
输出：最优分类的特征的index
'''


def chooseBestFeatureToSplit(dataSet):
    # 计算特征数量
    numFeatures = len(dataSet[0]) - 1  # the last column is used for the labels
    baseEntropy = calc_shannon_ent(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1
    for i in range(numFeatures):  # iterate over all the features
        # 创建唯一的分类标签列表
        featList = [example[i] for example in dataSet]  # create a list of all the examples of this feature
        uniqueVals = set(featList)  # get a set of unique values
        newEntropy = 0.0
        # 计算每种划分方式的信息熵
        for value in uniqueVals:
            subDataSet = split_data_set(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calc_shannon_ent(subDataSet)
        infoGain = baseEntropy - newEntropy  # calculate the info gain; ie reduction in entropy
        # 计算最好的信息增益，即infoGain越大划分效果越好
        if (infoGain > bestInfoGain):  # compare this to the best gain so far
            bestInfoGain = infoGain  # if better than current best, set to best
            bestFeature = i
    return bestFeature  # returns an integer


'''
投票表决函数
输入classList:标签集合，本例为：['yes', 'yes', 'yes', 'no', 'no']
输出：得票数最多的分类名称
'''


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    # 把分类结果进行排序，然后返回得票数最多的分类结果
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


'''
创建树的函数代码
输入：数据集和标签列表
输出：树的所有信息
'''


def createTree(dataSet, labels):
    # classList为数据集的所有类标签
    classList = [example[-1] for example in dataSet]
    # 停止条件1:所有类标签完全相同，直接返回该类标签
    if classList.count(classList[0]) == len(classList):
        return classList[0]  # stop splitting when all of the classes are equal
    # 停止条件2:遍历完所有特征时仍不能将数据集划分成仅包含唯一类别的分组，则返回出现次数最多的类标签
    if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    # 选择最优分类特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    # myTree存储树的所有信息
    myTree = {bestFeatLabel: {}}
    # 以下得到列表包含的所有属性值
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    # 遍历当前选择特征包含的所有属性值
    for value in uniqueVals:
        subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(split_data_set(dataSet, bestFeat, value), subLabels)
    return myTree



if __name__ == '__main__':
    '''
    计算给定数据集的香农熵/熵(集合信息的度量方式)
    '''
    dateSet, labes = create_data_set()
    shannonEnt = calc_shannon_ent(dateSet)
    # shannonEnt(熵)越高，则混合的数据也越多
    print(shannonEnt)
    print(split_data_set(dateSet, 0, 1))
    print(split_data_set(dateSet, 1, 1))
    print(split_data_set(dateSet, 0, 0))
    print(chooseBestFeatureToSplit(dateSet))
    # 输出：得票数最多的分类名称
    print(majorityCnt(['yes', 'yes', 'yes', 'no', 'no']))
    print(createTree(dateSet,labes))

