"""
encoding: utf-8
Author: MoncozGC
Date  : 2022/1/10 19:18
Desc  : 处理excel表单数据
"""
import pandas as pd

# 方法一: 默认读取第一个表单
# 这个会直接默认读取到这个Excel的第一个表单
# df = pd.read_excel("./datas/价格分析目录.xlsx")
# 默认读取前5行的数据
# data = df.head()
# 格式化输出
# print("获取到所有的值:\n{0}".format(data))

# 方法二: 通过指定表单名的方式来读取
# sheet_name: 指定sheet页的名称
# df = pd.read_excel("./datas/价格分析目录.xlsx", sheet_name='Sheet2')
# 默认读取前5行的数据
# # data = df.head()
# print("获取到所有的值:\n{0}".format(data))

# 方法三： 通过表单索引来指定访问的表单
# 可以通过索引或者表单名 同时指定多个
df = pd.read_excel('./datas/价格分析目录.xlsx', sheet_name=['sheet1', 'Sheet2'])
df = pd.read_excel('./datas/价格分析目录.xlsx', sheet_name=[0,1])
data = df.values
print("获取到所有的值:\n{0}".format(data))

