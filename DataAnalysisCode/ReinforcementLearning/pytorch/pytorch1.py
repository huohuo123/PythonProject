# pytorch和numpy之间的互相更换和比较。torch自称为神经网络的numpy
import torch
import numpy as np

# torch和numpy互相转换
np_data = np.arange(6).reshape((2, 3))
torch_data = torch.from_numpy(np_data)
tensor2array = torch_data.numpy()

print(
    '\nnumpy:', np_data,
    '\ntorch:', torch_data,
    '\ntensor2array:', tensor2array
)

# abs
data = [-1, -2, 1, 2]
tensor = torch.FloatTensor(data)
# 绝对值
print(
    '\nnp:', np.abs(data),
    '\ntorch:', torch.abs(tensor)
)
# 平均值
print(
    '\nnp:', np.mean(data),
    '\ntorch:', torch.mean(tensor)
)

data = [[1, 2], [3, 4]]
tensor = torch.FloatTensor(data)

# 矩阵相乘
print(
    '\nnumpuy:', np.matmul(data, data),
    '\ntorch:', torch.mm(tensor, tensor)
)
