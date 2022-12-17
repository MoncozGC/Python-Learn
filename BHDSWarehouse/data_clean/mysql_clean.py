# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/8/4 14:13
# Desc  : 数据清洗

import pandas as pd
import pymysql

if __name__ == '__main__':
    con = pymysql.connect(host="xxxx", port=3306, user="xxxx", password="xxxx", db="bhds_base")
    # 读取sql
    data_sql = pd.read_sql("select customer_bizscope from org_customer_nmpa limit 300", con, index_col='customer_bizscope')

    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 显示宽度无限长
    pd.set_option('display.width', None)

    # 存储
    # data_sql.to_csv("test.csv")

    print(data_sql)
