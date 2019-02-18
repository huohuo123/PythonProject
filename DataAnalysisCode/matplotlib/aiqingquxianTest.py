import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
# 2019年02月14日17:13:59 情人节，送与老公的大红心
# 中文配置 从系统找去想要显示的中文字体路径所在
# r表示正则表达的一个形式
font = FontProperties(fname=r"/System/Library/Fonts/STHeiti Medium.ttc", size=18)
plt.title('情人节快乐', fontproperties=font)
# linspace构建等差数列
# linspace()通过指定开始值、终值和元素个数创建表示等差数列的一维数组，
# 可以通过endpoint参数指定是否包含终值，默认值为True，即包含终值。
x = np.linspace(-1, 1, 200)
# 把函数分为上下两个部分
y1 = np.sqrt(1 - np.power(x, 2)) + np.power(np.square(x), 0.33)
y2 = -np.sqrt(1 - np.power(x, 2)) + np.power(np.square(x), 0.33)
# 设置一下x轴、y轴的刻度和坐标间距
# 通过构建等差数列，使心形更加好看
# arange()类似于内置函数range()，通过指定开始值、终值和步长创建表示等差数列的一维数组，
# 注意得到的结果数组不包含终值。
my_x_ticks = np.arange(-2, 2.5, 0.5)
my_y_ticks = np.arange(-2, 2.5, 0.5)
# r指定red.b指定blue
plt.plot(x, y1, color='r')
plt.plot(x, y2, color='r')
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
# 填充红心 alpha设置红色的深浅，range为0-1范围。
plt.fill_between(x, y1, y2, color='red', alpha=1.0)
plt.show()
