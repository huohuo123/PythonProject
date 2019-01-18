# 聚类 K-means应用
import numpy as np
# 加载PIL包，用于加载创建图片
import PIL.Image as image
from sklearn.cluster import KMeans


# 调用K-means所需参数
# 一般调用只需要给出n_clusters即可，init默认是k-means++,max_iter默认是300
# n_clusters:用于指定聚类中心的个数
# init:初始聚类中心的初始化方法
# max_iter:最大的迭代次数
def main(filePath):
    # 以二进制形式打开文件
    f = open(filePath, 'rb')
    data = []
    # 以列表形式返回图片像素值
    img = image.open(f)
    m, n = img.size
    # 将每个像素点颜色处理至0-1
    for i in range(m):
        # 范围内并存放入data
        for j in range(n):
            x, y, z = img.getpixel((i, j))
            data.append([x / 256.0, y / 256.0, z / 256.0])
    f.close()
    # 以矩阵形式返回data,以及图片大小
    return np.mat(data), m, n


if __name__ == '__main__':
    imgdata, row, col = main('../data/1.png')
