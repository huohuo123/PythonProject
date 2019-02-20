# Tensorflow的设计理念称之为计算流图，在编写程序时，首先构筑整个系统的graph，代码并不会直接生效，这一点和python的其他数值计算库（如Numpy等）不同，graph为静态的，类似于docker中的镜像
import tensorflow as tf

input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)
# module 'tensorflow' has no attribute 'mul' （用multiply来替代mul）
output = tf.multiply(input1, input2)

with tf.Session() as sess:
    # feed_dict类似于一个字典的形式，运行结果直接是7*2
    print(sess.run(output, feed_dict={input1: [7.], input2: [2.]}))
