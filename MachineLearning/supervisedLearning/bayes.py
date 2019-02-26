from math import log
import operator

'''
创建实验样本
'''


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    # 1代表侮辱性文字，0代表正常言论
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec


def createVocabList(dataSet):
    # 使用set创建不重复词表库
    vocabSet = set([])  # create empty set
    for document in dataSet:
        # 创建两个集合的并集
        vocabSet = vocabSet | set(document)  # union of the two sets
    return list(vocabSet)


# todo 不是很懂到底是什么意思 time:2019年02月24日11:27:48
def setOfWords2Vec(vocabList, inputSet):
    # 创建一个所包含元素都为0的向量
    returnVec = [0] * len(vocabList)
    # 遍历文档中的所有单词，如果出现了词汇表中的单词，则将输出的文档向量中的对应值设为1
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec


def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
            return returnVec

'''
朴素贝叶斯分类器训练函数(此处仅处理两类分类问题)
trainMatrix:文档矩阵
trainCategory:每篇文档类别标签
'''
# def trainNB0(trainMatrix, trainCategory):
#     numTrainDocs = len(trainMatrix)
#     numWords = len(trainMatrix[0])
#     pAbusive = sum(trainCategory) / float(numTrainDocs)
#     #初始化所有词出现数为1，并将分母初始化为2，避免某一个概率值为0
#     p0Num = ones(numWords);
#     p1Num = ones(numWords)  # change to ones()
#     p0Denom = 2.0;
#     p1Denom = 2.0  # change to 2.0
#     for i in range(numTrainDocs):
#         if trainCategory[i] == 1:
#             p1Num += trainMatrix[i]
#             p1Denom += sum(trainMatrix[i])
#         else:
#             p0Num += trainMatrix[i]
#             p0Denom += sum(trainMatrix[i])
#     p1Vect = log(p1Num / p1Denom)  # change to log()
#     p0Vect = log(p0Num / p0Denom)  # change to log()
#     return p0Vect, p1Vect, pAbusive


if __name__ == '__main__':
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    # 未排序但是无重复值的结果
    print(myVocabList)
    print(setOfWords2Vec(myVocabList, listOPosts[0]))
    print(setOfWords2Vec(myVocabList, listOPosts[3]))
