# encoding=utf-8
import numpy as np
import pandas as pd
from pylab import *
import xlrd
import openpyxl


def main():
    # series是pd的一种基本数据结构
    # DataFrame定义表格结构
    s = pd.Series([i * 2 for i in range(1, 11)])
    print(type(s))
    dates = pd.date_range("20190101", periods=8)
    # index：索引或类似数组，可以认为是主键；columns属性
    df = pd.DataFrame(np.random.randn(8, 5), index=dates, columns=list("ABCDE"))
    print(df)
    # 分别指定每个属性的值
    # df = pd.DataFrame({"A": 1, "B": pd.Timestamp("20190101"), "C": pd.Series(1, index=list(range(4)), dtype="float32"),
    #                    "D": np.array([3] * 4, dtype="float32"),
    #                    "E": pd.Categorical(["police", "student", "teacher", "doctor"])})
    #
    # print(df)

    # 基本操作
    # head打印前几行
    print(df.head(3))
    # tail打印后几行
    print(df.tail(3))
    # 打印主键那行
    print(df.index)
    print(df.values)
    # 转置
    print(df.T)
    # 属性 列排序
    print(df.sort_values("C"))
    # ascending=False降序
    print(df.sort_index(axis=1, ascending=False))

    # 选择
    # 切片几种方式
    print(df["A"])
    print(df["20190101":"20190104"])
    print(df.loc[dates[0]])
    print(df.loc["20190101":"20190102", ["B", "D"]])
    print(df.at[dates[0], "C"])

    print(df.iloc[1:3, 2:4])
    print(df.iloc[1, 4])
    print(df.iat[1, 4])

    # 填入条件筛选
    print(df[df.B > 0][df.A < 0])
    print(df[df["E"].isin([1, 2])])

    # set
    s1 = pd.Series(list(range(10, 18)), index=pd.date_range("20190101", periods=8))
    df["F"] = s1
    print(df)
    # 对单个值进行修改
    df.at[dates[0], "A"] = 0

    # 缺失值处理
    df1 = df.reindex(index=dates[:4], columns=list("ABCD") + ["G"])
    # 只对G列的第一行，第二行赋值
    df1.loc[dates[0]:dates[1], "G"] = 1
    print(df1)
    # 摒弃处理
    print(df1.dropna())
    # 填充处理
    print(df1.fillna(value=1))

    # 表统计和整合
    # 均值
    print(df1.mean())
    # 方差
    print(df1.var())
    s = pd.Series([1, 2, 4, np.nan, 5, 7, 9, 10], index=dates)
    print(s)
    # 多两行Nan值
    print(s.shift(2))
    # 下一个值-上一个值
    print(s.diff())
    # 每个值在表格中出现的次数
    print(s.value_counts())
    # 累加值
    print(df.apply(np.cumsum))
    # 极差，最大值减最小值
    print(df.apply(lambda x: x.max() - x.min()))

    # 表格拼接
    # 前三行与后三行拼接
    pieces = [df[:3], df[-3:]]
    print(pd.concat(pieces))
    left = pd.DataFrame({"key": ["x", "y"], "values": [1, 2]})
    right = pd.DataFrame({"key": ["x", "z"], "values": [3, 4]})
    print("left:", left)
    print("right:", right)
    # 类似于sql中的join函数 left,inner,outer
    print(pd.merge(left, right, on="key", how="left"))
    # group by
    df3 = pd.DataFrame({"A": ["a", "b", "c", "b"], "B": list(range(4))})
    print(df3)
    print(df3.groupby("A").sum())

    # Reshape 交叉分析，透视
    import datetime
    df4 = pd.DataFrame({'A': ['one', 'one', 'two', 'three'] * 6,
                        'B': ['a', 'b', 'c'] * 8,
                        'C': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 4,
                        'D': np.random.randn(24),
                        'E': np.random.randn(24),
                        'F': [datetime.datetime(2017, i, 1) for i in range(1, 13)] +
                             [datetime.datetime(2017, i, 15) for i in range(1, 13)]})
    # values:输出值，index:输出项，columns：列值
    print(pd.pivot_table(df4, values="D", index=["A", "B"], columns=["C"]))

    # Time Series
    t_exam = pd.date_range("20190101", periods=10, freq="S")
    print(t_exam)

    # Graph
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("20190101", periods=1000))
    ts = ts.cumsum()

    ts.plot()
    show()

    # File
    # df6 = pd.read_csv("/Users/huoyajing/StudyingSelf/python/data/test.csv")
    df7 = pd.read_excel("/Users/huoyajing/StudyingSelf/python/data/test.xlsx", "Sheet1")
    df6=pd.read_csv("../data/test.csv")
    print(df6)
    # print(df7)
    df6.to_csv("../data/test2.csv")
    df7.to_excel("../data/test2.xlsx")


if __name__ == '__main__':
    main()
