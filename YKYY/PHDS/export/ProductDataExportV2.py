# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/27 16:49
# Desc  : 商品数据 改为openpyxl库导出成EXCEL, 以及通过SQL的方式改变中文的编码

# 说明：需要写入的是二维列表target_data
# 将数据写入excel表格

import os
import sys
from datetime import datetime

import openpyxl
import pymssql  # 引入pymssql模块

# 下边链接信息为虚拟的，大家只要对号入座填写自己的数据库连接信息即可
host = 'xxx'
username = 'root'
passwd = 'root'
db = 'hydee'
port = 3306
charset = "utf8"

current_dir = os.path.dirname(sys.argv[0]) + "\\"
nowDate = datetime.now().strftime('%Y%m%d%H%M%S')

# 表头
fields = ["商品码(必填)", "通用名(必填)", "商品名", "商品规格(必填)", "包装单位(必填)", "剂型(必填)", "产地", "生产厂家(必填)", "批准文号(必填)", "国际标准码(必填)"]


def wr_Excel():
    # 连数据库，读取数据
    conn = pymssql.connect('xxxx:11118', 'root', 'root', 'hydee', charset="utf8")
    cur = conn.cursor()
    sql = """select 
    CONVERT(nvarchar(255), a.wareid),
    CONVERT(nvarchar(255), warename),
    CONVERT(nvarchar(255), waresimname),
    CONVERT(nvarchar(255), warespec),
    CONVERT(nvarchar(255), a.wareunit),
    CONVERT(nvarchar(255), c.classname),
    CONVERT(nvarchar(255), prod_add),
    CONVERT(nvarchar(255), producer),
    CONVERT(nvarchar(255), fileno),
    CONVERT(nvarchar(255), barcode)
    from u_ware_q a,u_ware_ext b ,v_ware_class c 
    where a.wareid=b.wareid and a.wareid=c.wareid and c.parentcode='03' """
    cur.execute(sql)
    sql_result = cur.fetchall()
    cur.close()
    conn.close()
    # 写 excel
    book = openpyxl.Workbook()
    sheet = book.active

    sheet.append(fields)
    for i in sql_result:
        row = list(i)
        # if all(i):
        #     row[3] = i[3].encode('latin1').decode('cp936')
        #     row[4] = i[4].encode('latin1').decode('cp936')
        #     row[5] = i[5].encode('latin1').decode('cp936')
        #     row[6] = i[6].encode('latin1').decode('cp936')
        #     row[7] = i[7].encode('latin1').decode('cp936')
        #     row[8] = i[8].encode('latin1').decode('cp936')
        #     row[9] = i[9].encode('latin1').decode('cp936')
        # print(row)
        # print(all(i))
        sheet.append(row)

    save_dir = current_dir + "商品数据_" + "%s.xlsx" % nowDate
    book.save(save_dir)
    print("文件保存: %s", save_dir)


if __name__ == '__main__':
    wr_Excel()
