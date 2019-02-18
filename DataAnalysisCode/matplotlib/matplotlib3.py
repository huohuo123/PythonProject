# 2019年02月15日17:16:31

# 最常用的一个模块
import matplotlib.pyplot as plt
import numpy as np

# x为-1到1 50个点
x = np.linspace(-1, 1, 50)
# 要展示的一次函数
y1 = 2 * x + 1
y2 = x ** 2
# plot 展示
# 有几个figure就可以创建几个窗口
plt.figure()
# plt.plot(x, y1)
# # linewidth线条宽度 linestyle样式
# plt.plot(x, y2, linewidth=1.0, color='red', linestyle='--')

# 控制x,y的展示范围
plt.xlim(-5, 5)
plt.ylim(-5, 5)

# plt.xlabel('I am x')
# plt.ylabel('I am y')

# ticks重新更换
# new_ticks = np.linspace(-1, 2, 5)
# plt.xticks(new_ticks)
# 对y的ticks进行单独设置,由数字设置成文字显示
# r'$really\ bad$' r表示正则表达的一种形式 $$只是一种数字形式展示，用于展示样式统一
# 一个转制符很厉害，可以由英文转成数学形式 \alpha
# plt.yticks([-2, -1.8, -1, 1.22, 5],
#            [r'$really\ bad$', r'$bad\ \alpha$', r'$normal$', r'$good$', r'$really\ good$'])

# label及需要设置的名字；legend则是最简单的线条标注
l1 = plt.plot(x, y1, label='up')
# linewidth线条宽度 linestyle样式
l2 = plt.plot(x, y2, linewidth=1.0, color='red', linestyle='--', label='down')
# legend()图例标示
plt.legend()
# 设置右侧和上册的轴消失，左侧和下侧轴移动
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

# 对轴上的数值显示设定（tick的能见度）
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.7))

# annotation 注解，即对某一个点的标注
x0 = 1
y0 = 2 * x0 + 1
# scatter代表一个点 s表示点的大小
plt.scatter(x0, y0, s=50, color='b')
# 标记的竖线
plt.plot([x0, x0], [y0, 0], 'k--', lw=2.5)

plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30), textcoords='offset points',
             fontsize=16, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

plt.show()
