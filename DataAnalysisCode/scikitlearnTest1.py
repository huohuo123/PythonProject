import numpy as np
import pandas as pd


def main():
    # 预处理

    from sklearn.datasets import load_iris
    iris = load_iris()
    print(iris)
    # 类似于json解析
    print(iris["data"])
    print(len(iris["data"]))
    # 把数据分为测试数据，验证数据，test_size=0.2表示验证数据集占20%；random_state=1随机的选择20%的数据
    from sklearn.model_selection import train_test_split
    train_data, test_data, train_target, test_target = train_test_split(iris.data, iris.target, test_size=0.2,
                                                                        random_state=1)

    # 建模

    # 引入决策树
    # todo 决策树深入理解
    from sklearn import tree
    clf = tree.DecisionTreeClassifier(criterion="entropy")
    # fit train_data,train_target两者建立一种决策树的关系
    clf.fit(train_data, train_target)
    y_pred = clf.predict(test_data)

    # 验证
    from sklearn import metrics
    # 准确率方式验证
    print(metrics.accuracy_score(y_true=test_target, y_pred=y_pred))
    # 混淆矩阵验证方式
    print(metrics.confusion_matrix(y_true=test_target, y_pred=y_pred))

    # 输出
    with open("../data/tree.dot", "w") as fw:
        tree.export_graphviz(clf, out_file=fw)


if __name__ == '__main__':
    main()
