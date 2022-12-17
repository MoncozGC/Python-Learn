# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/8/4 14:13
# Desc  : 数据清洗

import pandas as pd

from utils.comm_util import *

# import numpy as np
# import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('qunar_freetrip.csv', index_col=0)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 显示宽度无限长
    pd.set_option('display.width', None)
    # 输出数据
    # print(df.head(2))
    # # 查看数据形状
    # print(df.shape)
    # # 查看数据结构
    # print(df.info())
    # # 描述统计信息, 只显示数值型的描述
    # print(df.describe())

    print(df.columns)
    print_ts(df['价格'])

    # 去除列的前后空格
    # 1.1 转换为数组
    cols = df.columns.values
    # 使用推导式去除空格, strip去重前后空格
    ds = [x.strip() for x in cols]
    print(ds)

