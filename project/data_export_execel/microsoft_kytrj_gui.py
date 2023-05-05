# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/5/4
# Desc  : 快易通医药软件, Microsoft Access数据导出 提供GUI界面
from tkinter import Tk, Label, Entry, Button, Text, StringVar
from tkinter import messagebox

import pandas as pd
import pyodbc


def query_data():
    start_date = start_date_var.get()
    end_date = end_date_var.get()

    if not start_date or not end_date:
        messagebox.showwarning("警告", "请填写开始和结束日期")
        return

    # 根据您的环境更改数据库文件的路径
    access_db_file = r'../data/zxdzcf_20230504'

    # 设置连接字符串
    conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + access_db_file + ';'
    )

    # 建立数据库连接
    conn = pyodbc.connect(conn_str)

    # 编写 SQL 查询
    sql_query = f"SELECT TOP 10 处方编号,姓名,年龄,性别,日期,电话,住址,临床表现,诊断,剂数,执业医师,方名,中医处方,西医处方,用法,过敏史,中医验方,西医验方,处理 FROM bingli WHERE 日期 >= '{start_date}' AND 日期 <= '{end_date}'"

    print(sql_query)
    # 使用 pandas 从 Access 数据库中读取数据并将其存储到 DataFrame
    df = pd.read_sql(sql_query, conn)

    # 关闭连接
    conn.close()

    # 将 DataFrame 保存到 Excel 文件
    excel_file = '病例导出.xlsx'
    df.to_excel(excel_file, index=False)
    print("Export succeeded")


root = Tk()
root.title("Microsoft Access 查询")

Label(root, text="开始日期 (MM-DD-YYYY)").grid(row=0, column=0)
Label(root, text="结束日期 (MM-DD-YYYY)").grid(row=1, column=0)

start_date_var = StringVar()
end_date_var = StringVar()

start_date_entry = Entry(root, textvariable=start_date_var)
start_date_entry.grid(row=0, column=1)

end_date_entry = Entry(root, textvariable=end_date_var)
end_date_entry.grid(row=1, column=1)

query_button = Button(root, text="查询", command=query_data)
query_button.grid(row=2, column=0, columnspan=2)

result_text = Text(root, wrap="none", width=80, height=20)
result_text.grid(row=3, column=0, columnspan=2)

root.mainloop()
