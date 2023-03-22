# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/24 21:33
# Desc  : https://blog.csdn.net/weixin_44322778/article/details/102477108

import os

import pyodbc
import xlwt

# from sqltest import row

connect = pyodbc.connect('DRIVER={SQL Server};SERVER=(xxxx:11118);DATABASE=hydee;UID=root;PWD=root')
cursor = connect.cursor()
sql = """select a.wareid,warename,waresimname,warespec,a.wareunit,c.classname,prod_add,producer,fileno,barcode
from u_ware_q a,u_ware_ext b ,v_ware_class c 
where a.wareid=b.wareid and a.wareid=c.wareid and c.parentcode='03' """
count = cursor.execute(sql)
row = cursor.fetchall()  # sql语句执行结果的获取，如果需要一次获取多条记录，可以使用cursor.fetchall()方法
# if row:
# print (row)

connect.commit()
connect.close()


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def write_excel():
    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet
    data_sheet = workbook.add_sheet('201903', cell_overwrite_ok=True)
    # 列表格式数据
    excelData = row
    # 定义循环下标
    index = 0

    file_style = xlwt.XFStyle()
    for i in excelData:
        # 每一列的内容(i)
        for x, item in enumerate(i):
            # 下标(x)，单元元素(item)
            #  data_sheet.write(index, x, item, set_style('Times New Roman',220, True))
            data_sheet.write(index, x, item, file_style)
        index += 1
        # sys.exit();
        # 保存文件
    workbook.save('PJDM.xls')
    print(os.getcwd())


if __name__ == '__main__':
    write_excel()
