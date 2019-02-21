
import torch
from torch.autograd import Variable

tensor=torch.FloatTensor([[1,2],[3,4]])
# 一个计算节点
variable=Variable(tensor,requires_grad=True)

t_out=torch.mean(tensor*tensor)
v_out=torch.mean(variable*variable)

v_out.backward()
print(t_out)
print(v_out)
print(variable.grad)