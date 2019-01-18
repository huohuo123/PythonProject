# encoding=utf-8
import numpy as np
# 人工神经网络，各个层的容器
from keras.models import Sequential
# dense:全连接层;Activation:激活函数
from keras.layers import Dense, Activation
# 随机梯度下降优化器
from keras.optimizers import SGD


def main():
    # 数据集
    from sklearn.datasets import load_iris
    iris = load_iris()
    # 标签化，比如把数值用二进制表示
    from sklearn.preprocessing import LabelBinarizer
    print(LabelBinarizer().fit_transform(iris["target"]))
    # 把数据分为测试数据，验证数据，test_size=0.2表示验证数据集占20%；random_state=1随机的选择20%的数据
    from sklearn.model_selection import train_test_split
    train_data, test_data, train_target, test_target = train_test_split(iris.data, iris.target, test_size=0.2,
                                                                        random_state=1)
    labels_train = LabelBinarizer().fit_transform(train_target)
    labels_test = LabelBinarizer().fit_transform(test_target)

    # 网络结构
    model = Sequential(
        [
            Dense(5, input_dim=4),
            Activation("relu"),
            Dense(3),
            Activation("sigmoid")
        ]
    )

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss="categorical_crossentropy")
    # 预测200轮，每轮用40个数据
    # 新版本中，nb_epoch改为epochs使用
    model.fit(train_data, labels_train, epochs=200, batch_size=40)
    print(model.predict_classes(test_data))
    # 存储
    model.save_weights("../data/w")

if __name__ == '__main__':
    main()
