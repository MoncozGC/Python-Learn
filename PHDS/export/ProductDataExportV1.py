# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/24 21:35
# Desc  : 商品数据导出
# EXE文件输出: pyinstaller -F "F:\F-Data Files\Server Backup\Desktop-YKYY\Work File\IntelliJ IDEA\YKYY-PyCharm\Python-Employ\PHDS\export\sqlServerExport03.
import os
import sys
from datetime import datetime

import pymssql  # 引入pymssql模块
import xlwt  # 引入xlwt模块

# 表头
fields = ["商品码(必填)", "通用名(必填)", "商品名", "商品规格(必填)", "包装单位(必填)", "剂型(必填)", "产地", "生产厂家(必填)", "批准文号(必填)", "国际标准码(必填)"]

# Format Date
style_datetme = xlwt.XFStyle()
style_datetme.num_format_str = 'M/D/YY hh:mm'

# 为样式创建字体
font = xlwt.Font()
font.height = 250  # 字体大小
font.bold = True  # 居中
style_datetme.font = font

# 对齐
alignment = xlwt.Alignment()
alignment.horz = 0x02  # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
alignment.vert = 0x01  # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
alignment.wrap = 1  # 设置自动换行
style_datetme.alignment = alignment

# 背景
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern.pattern_fore_colour = 57  # 给背景颜色赋值
style_datetme.pattern = pattern  # 把背景颜色加到表格样式里去

# 写入excel
book = xlwt.Workbook()
sheet = book.add_sheet('sheet1')

# 设置单元格宽度
for i in range(len(fields)):
    sheet.col(i).width = 256 * 25  # Set the column width 设置第一列列宽

first_col = sheet.col(0)  # 获取第一列
first_col.width = 256 * 20  # 设置第一列列宽
tall_style = xlwt.easyxf('font:height 620')  # 设置行高
first_row = sheet.row(0)  # 获取sheet页的第一行
first_row.set_style(tall_style)  # 给第一行设置tall_style样式，也就是行高

# 当前运行文件路径
# current_dir = os.path.abspath(os.path.dirname(__file__)) + "\\"
current_dir = os.path.dirname(sys.argv[0]) + "\\"

# bat执行脚本
# 有哪些参数
for s in range(1, len(sys.argv)):
    # 对参数进行处理
    print("参数{0}为：{1}".format(s, sys.argv[s]))

# 数据库登录
# ip = input('ip: ')
# port = input('port: ')
# users = input('user: ')
# pwd = input('pwd: ')
# databases = input('db: ')
# bat文件输入
# ip = sys.argv[1]
# port = sys.argv[2]
# users = sys.argv[3]
# pwd = sys.argv[4]
# databases = sys.argv[5]
# 服务器名,端口,账户,密码,数据库名
connect = pymssql.connect('xxxx:11118', 'root', 'root', 'hydee', charset="utf8")


# connect = pymssql.connect('xxxx', '11118', users, pwds, 'hydee', charset="utf8")
# connect = pymssql.connect(host=ip, port=port, user=users, password=pwd, database=databases, charset="utf8")
# connect = pymssql.connect(host=ip, port=port, user=users, password=pwd, database=databases, charset="utf8")


def export_excel():
    if connect:
        print("数据库连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql = """select a.wareid,warename,waresimname,warespec,a.wareunit,c.classname,prod_add,producer,fileno,barcode
from u_ware_q a,u_ware_ext b ,v_ware_class c 
where a.wareid=b.wareid and a.wareid=c.wareid and c.parentcode='03' """
    cursor.execute(sql)  # 执行sql语句

    # fields = [field[0] for field in cursor.description]  # 获取所有字段名
    print(fields, len(fields))
    all_data = cursor.fetchall()  # 所有数据
    aa = datetime.now().strftime('%Y%m%d%H%M%S')

    # 首行
    for col, field in enumerate(fields):
        sheet.write(0, col, field, style_datetme)

    row = 1

    en3, en4, en5, en6, en7, en8, en9 = '', '', '', '', '', '', ''

    # for data in all_data:
    #     if not data[3] or not data[4] or not data[5] or not data[6] or not data[7] or not data[8] or not data[9]: continue
    #     en3 = data[3].encode('latin1').decode('cp936')
    #     en4 = data[4].encode('latin1').decode('cp936')
    #     en5 = data[5].encode('latin1').decode('cp936')
    #     en6 = data[6].encode('latin1').decode('cp936')
    #     en7 = data[7].encode('latin1').decode('cp936')
    #     en8 = data[8].encode('latin1').decode('cp936')
    #     en9 = data[9].encode('latin1').decode('cp936')

    for data in all_data:
        # 如果有数据为空则不进行编码转换, 否则会报错
        if all(data):
            en3 = data[3].encode('latin1').decode('cp936')
            en4 = data[4].encode('latin1').decode('cp936')
            en5 = data[5].encode('latin1').decode('cp936')
            en6 = data[6].encode('latin1').decode('cp936')
            en7 = data[7].encode('latin1').decode('cp936')
            en8 = data[8].encode('latin1').decode('cp936')
            en9 = data[9].encode('latin1').decode('cp936')
        for col, field in enumerate(data):
            # 单独处理编码格式
            if col == 3:
                sheet.write(row, col, en3)
            elif col == 4:
                sheet.write(row, col, en4)
            elif col == 5:
                sheet.write(row, col, en5)
            elif col == 6:
                sheet.write(row, col, en6)
            elif col == 7:
                sheet.write(row, col, en7)
            elif col == 8:
                sheet.write(row, col, en8)
            elif col == 9:
                sheet.write(row, col, en9)
            else:
                sheet.write(row, col, field)

        row += 1

    save_dir = current_dir + "商品数据_" + "%s.xls" % aa
    book.save(save_dir)
    print("文件保存地址: ", save_dir)

    print("Export to excel success!")


if __name__ == '__main__':
    # export data from SQL server
    export_excel()

    # close database connection
    connect.close()

    # 打包使用
    # input('Press Enter to exit…')
