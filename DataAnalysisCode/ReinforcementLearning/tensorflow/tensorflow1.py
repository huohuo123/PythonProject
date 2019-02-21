# 预测一个线性的直线  测试的结果，逐渐的接近0.1和0.3
import tensorflow as tf
import numpy as np

# create data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3

# create tensorflow structure（创建结构）
# Weights可能是一个矩阵的形式，所以大写；初始值范围-1到1
Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
# biases初始值为0
biases = tf.Variable(tf.zeros([1]))
# 预测的y
y = Weights * x_data + biases

loss = tf.reduce_mean(tf.square(y - y_data))
# 优化器，通过优化器减少误差，GradientDescentOptimizer最基础，原始的优化器
optimizer = tf.train.GradientDescentOptimizer(0.5)
# 减少误差
train = optimizer.minimize(loss)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

for step in range(201):
    sess.run(train)
    # 每隔20步打印一下
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))
