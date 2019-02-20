# session 的两种打开方式
import tensorflow as tf
import numpy as np

matrix1 = tf.constant([[3, 3]])
matrix2 = tf.constant([[2], [2]])
# matrix muitiply 类似于 np.dot(m1,m2)
product = tf.matmul(matrix1, matrix2)

# session会话控制有两种形式
# # method 1
# sess=tf.Session()
# result=sess.run(product)
# print(result)
# sess.close()

# method 2  通过with形式直接就可以关闭session，而无需手动关闭
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)
