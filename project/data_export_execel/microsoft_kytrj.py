# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/5/4
# Desc  : 快易通医药软件, Microsoft Access本地数据导出
import pandas as pd
import pyodbc

if __name__ == '__main__':
    # 根据您的环境更改数据库文件的路径
    access_db_file = r'../data/zxdzcf_20230504'  # .mdb 文件或 .accdb 文件

    # 设置连接字符串
    conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + access_db_file + ';'
    )

    # 建立数据库连接
    conn = pyodbc.connect(conn_str)

    # 编写 SQL 查询
    sql_query = "SELECT TOP 10 处方编号,姓名,年龄,性别,日期,电话,住址,临床表现,诊断,剂数,执业医师,方名,中医处方,西医处方,用法,过敏史,中医验方,西医验方,处理  FROM bingli "

    # 使用 pandas 从 Access 数据库中读取数据并将其存储到 DataFrame
    df = pd.read_sql(sql_query, conn)

    # 将 DataFrame 保存到 Excel 文件
    excel_file = '病例导出.xlsx'
    df.to_excel(excel_file, index=False)

    # 关闭连接
    conn.close()

    print(f"数据已保存到 {excel_file}")
