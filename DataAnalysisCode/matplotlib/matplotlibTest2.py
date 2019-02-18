# 子图与多种图形绘制
# 常用图表
# 有点太复杂，目前看不懂2019年02月15日17:13:46
import numpy as np

import matplotlib.pyplot as plt


def main():
    # 散点图 scatter
    fig = plt.figure()
    # 表示散点图画在此区域内
    ax = fig.add_subplot(3, 3, 1)
    n = 102
    # 随机数
    X = np.random.normal(0, 1, n)
    Y = np.random.normal(0, 1, n)
    # 上色，Y除以X(颜色展示）
    T = np.arctan2(Y, X)
    # 指定显示范围
    # plt.axes([0.025, 0.025, 0.95, 0.95])
    # 用来画散点的，s表示大小，sise;c表示color
    ax.scatter(X, Y, s=75, c=T, alpha=.5)
    plt.xlim(-1.5, 1.5)
    plt.xticks([])
    plt.ylim(-1.5, 1.5)
    plt.yticks([])
    plt.axis()
    plt.title('scatter')
    plt.xlabel('x')
    plt.ylabel('y')

    # 柱状图 bar
    # fig.add_subplot(332)

    ax = fig.add_subplot(332)
    n = 10
    # 构造的数列，从0-9
    X = np.arange(n)
    # 随机数
    Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
    Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
    # 画出来，+Y1表示画在上面
    ax.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
    # 画出来，-Y2表示画在下面
    ax.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')
    for x, y in zip(X, Y1):
        # Y1进行注释，x+0.4表示延x轴正方向0.4，y+0.05表示延y轴正方向移0.05，va='bottom'表示图在文字下面
        plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center',
                 va='bottom')
    for x, y in zip(X, Y2):
        plt.text(x + 0.4, -y - 0.05, '%.2f' % y, ha='center', va='top')

    # 饼图 Pie
    fig.add_subplot(333)
    n = 20
    # 全域的变量，为1
    Z = np.ones(n)
    # 最后一个变量设为2
    Z[-1] *= 2
    # Z表示每块儿的值，explode = Z * .05表示每个扇形离中心的距离，labels为显示的值，colors显示的颜色（以灰度形式）
    plt.pie(Z, explode=Z * .05, labels=['%.2f' % (i / float(n)) for i in range(n)],
            colors=['%f' % (i / float(n)) for i in range(n)])
    # 设为正的圆形
    plt.gca().set_aspect('equal')
    plt.xticks([]), plt.yticks([])

    # 极坐标 polar
    # fig.add_subplot(334)
    # 极坐标形式显示,polar=true
    fig.add_subplot(334, polar=True)
    n = 20
    theta = np.arange(0.0, 2 * np.pi, 2 * np.pi / n)
    # 半径
    radii = 10 * np.random.rand(n)
    # plt.plot(theta, radii)
    plt.polar(theta, radii)

    # 热图 heatmap
    # colormap，上色
    from matplotlib import cm
    fig.add_subplot(335)
    data = np.random.rand(3, 3)
    cmap = cm.Blues
    # interpolation = 'nearest':离最近的差值
    map = plt.imshow(data, cmap=cmap, aspect='auto', interpolation='nearest', vmin=0, vmax=1)
    # 3D图
    from mpl_toolkits.mplot3d import Axes3D
    ax = fig.add_subplot(336, projection='3d')
    # 坐标（1，1，3），size为100
    ax.scatter(1, 1, 3, s=100)

    # 热力图
    fig.add_subplot(313)

    def f(x, y):
        return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)

    n = 256
    x = np.linspace(-3, 3, n)
    y = np.linspace(-3, 3, n)
    X, Y = np.meshgrid(x, y)
    # 热力图的函数
    plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap=plt.cm.hot)
    plt.savefig("./fig.png")

    plt.show()


if __name__ == '__main__':
    main()
