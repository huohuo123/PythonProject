import numpy as np
from pylab import *


def main():
    # todo 需要理解一下数学的积分问题了。
    # 积分模块
    # quad:一重积分；dblquad:二重积分；nquad：n维积分
    from scipy.integrate import quad, dblquad, nquad
    # np.inf代表正无穷
    # 结果第一个数值代表运算结果，第二个数值代表误差
    print(quad(lambda x: np.exp(-x), 0, np.inf))
    # 求二重积分 然后给t,x赋积分区间
    # lambda是匿名函数
    print(dblquad(lambda t, x: np.exp(-x * t) / t ** 3, 0, np.inf, lambda x: 1, lambda x: np.inf))

    def f(x, y):
        return x * y

    def bound_y():
        return [0, 0.5]

    def bound_x(y):
        return [0, 1 - 2 * y]

    print(nquad(f, [bound_x, bound_y]))

    # todo 极值目前也体会不了
    from scipy.optimize import minimize

    def rosen(x):
        return sum(100.0 * (x[1:] - x[:1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2)

    x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
    # nelder-meadd单纯形法
    res = minimize(rosen, x0, method="nelder-mead", options={"xtol": 1e-8, "disp": True})
    print("ROSE MINI:", res.x)

    def func(x):
        return (2 * x[0] * x[1] + 2 * x[0] - x[0] ** 2 - 2 * x[1] ** 2)

    # 定义的偏导数
    def func_deriv(x):
        dfdx0 = -(-2 * x[0] + 2 * x[1] + 2)
        dfdx1 = -(2 * x[0] - 4 * x[1])
        return np.array([dfdx0, dfdx1])

    # 约束条件，“jac”:雅可比行列式
    cons = ({'type': 'eq', 'fun': lambda x: np.array([x[0] ** 3 - x[1]]),
             'jac': lambda x: np.array([3.0 * (x[0] ** 2.0), -1.0])},
            {'type': 'ineq', 'fun': lambda x: np.array([x[1] - 1]), 'jac': lambda x: np.array([0.0, 1.0])})
    # constraints约数条件
    res = minimize(func, [-1.0, 1.0], jac=func_deriv, constraints=cons, method='SLSQP', options={'disp': True})
    print('RESTRICT:', res)

    # 优化器求根
    from scipy.optimize import root

    def fun(x):
        return x + 2 * np.cos(x)

    sol = root(fun, 10)
    print('ROOT:', sol.x, ', FUN:', sol.fun)

    x = np.linspace(0, 1, 10)
    y = np.sin(2 * np.pi * x)
    # 引入插值算法模块，interp1d为一维插值
    from scipy.interpolate import interp1d
    # 3次函数差值
    li = interp1d(x, y, kind='cubic')
    x_new = np.linspace(0, 1, 50)
    y_new = li(x_new)
    figure()
    # 红色表示原数据
    plot(x, y, 'r')
    # 黑色表示新数据
    plot(x_new, y_new, 'k')
    print(y_new)
    show()

    # 线性函数与矩阵的分解
    from scipy import linalg as lg
    arr = np.array([[1, 2], [3, 4]])
    # 行列式
    print('Det:', lg.det(arr))
    # 逆矩阵
    print('Inv:', lg.inv(arr))
    b = np.array([6, 14])
    # 解方程
    print('Sol:', lg.solve(arr, b))
    # 特征值 和 特征向量
    print('Eig:', lg.eig(arr))
    # 矩阵的四种分解
    print('LU:', lg.lu(arr))
    print('QR:', lg.qr(arr))
    print('SVD:', lg.svd(arr))
    print('Schur:', lg.schur(arr))


if __name__ == '__main__':
    main()
