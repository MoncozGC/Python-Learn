"""
encoding: utf-8
Author: MoncozGC
Date  : 2022/1/10 20:02
Desc  : Excel操作行列
"""
import pandas as pd

# 1：读取指定行
# 这个会直接默认读取到这个Excel的第一个表单
df = pd.read_excel('./datas/价格分析目录.xlsx')
# 0表示第一行 这里读取数据并不包含表头. 嵌套中括号可以读取指定多行. 下标都从零开始
data = df.iloc[[1, 2, 3]].values
# print("读取指定行的数据：\n{0}".format(data))

# 指定读取列
data = df.iloc[0, 2]
company_std_cfy_sku_num_map = {}
for sku in company_std_cfy_sku_num_map:
    print(sku)
# print("读取指定行的数据：\n{0}".format(data))
