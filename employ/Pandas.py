# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/2/9 14:46
# Desc  : Pandas的使用

import pandas as pd
import numpy as np

if __name__ == '__main__':
    # pd.Series 函数来创建Series对象
    # 第一个参数是存储的数据，这里是 Numpy 随机生成的一维数组。
    # 第二个参数index是数据对应的索引。在 Python list或 Numpy 中数组的索引都是数字，也称为下标，但在 Pandas 中索引可以是任意类型。
    array = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
    print(array)
    print("-----")

    # DataFrame 是二维结构, 类似于Excel或数据库总的表
    # 用字典d创建DataFrame对象，d中的两个键值对作为DataFrame两列。键作为列名，值是Series对象作为列值
    d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
         'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
    # 创建DataFrame对象
    df = pd.DataFrame(d)
    print(df)

    print("-----查看行索引")
    # 查看行索引
    print(df.index)
    # 查看列索引
    print("-----查看列索引")
    print(df.columns)
    # 根据首尾查看数据
    print("-----首尾查看数据")
    print(df.head(2))
    print(df.tail(2))
    # 查看每列统计摘要
    print("-----查看每列统计摘要")
    print(df.describe)

    index = pd.Index(['e', 'd', 'a', 'b'])
    columns = pd.Index(['A', 'B', 'C'], name='cols')
    df = pd.DataFrame(np.random.randn(4,3),)
