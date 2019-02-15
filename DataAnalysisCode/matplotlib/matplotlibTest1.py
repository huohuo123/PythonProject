# encoding=utf-8
# 基本绘图绘制
import numpy as np

import matplotlib.pyplot as plt


def main():
    # 绘制线
    # x轴  包含256个点，=true,包含最后一个
    x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    # 余弦和正弦函数
    c, s = np.cos(x), np.sin(x)
    plt.figure(1)
    # plt.plot(x, c)
    # 指定样式
    plt.plot(x, c, color="red", linewidth=1.0, linestyle="-", label="COS", alpha=0.5)
    # r指定red,b指定blue
    plt.plot(x, s, "b*", label="SIN", linewidth=1.0)
    # 标题
    plt.title("COS && SIN")
    # 设置横轴和纵轴
    ax = plt.gca()
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    # 数字样式和位置显示,感觉不用设置，估计是新版本优化的原因，很漂亮
    # ax.xaxis.set_ticks_position("bottom")
    # ax.xaxis.set_ticks_position("left")
    # 横轴设置,xticks两个数组，数组1：横轴需要标示的位置 数组2：标示的内容
    plt.xticks([-np.pi, -np.pi / 2.0, 0, np.pi / 2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
    # 从-1到1，设置5个点，且包含最后一个值
    plt.yticks(np.linspace(-1, 1, 5, endpoint=True))
    # 字体大小设置
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(16)
        # label小方框的内容，背景颜色：白，不要边的颜色，透明度为0.2
        label.set_bbox(dict(facecolor="blue", edgecolor="None", alpha=0.2))
    # 左上角线条说明
    plt.legend(loc="upper left")
    # 网格线
    plt.grid()
    # 显示范围,其实就是部分扩大化
    # plt.axis([-1,1,-0.5,1])
    # todo 填充显示不出来
    plt.fill_between(x, s, c, color='green', alpha=0.25)
    # 在t=1的地方，进行注释添加
    t = 1
    # 两点连线，y：黄色
    # (t, 0),(t, np.cos(t))
    plt.plot([t, t], [0, np.cos(t)], 'y', linewidth=3, linestyle='--')
    # 标注，内容“cos(1)”,从xytext（xytext，以textcoords的形式，从xy移动（+10, +30））指向点xy,样式为arrowprops:弧度为0.2
    # textcoords相对位置
    plt.annotate("cos(1)", xy=(t, np.cos(1)), xycoords="data", xytext=(+10, +30),
                 textcoords="offset points", arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))
    plt.show()


if __name__ == '__main__':
    main()
