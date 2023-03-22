# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/24 21:35
# Desc  : https://codeantenna.com/a/GFvpVOc3yG

import pymssql
import xlwt

# server    数据库服务器名称或IP
# user      用户名
# password  密码
# database  数据库名称
conn = pymssql.connect('xxxx:11118', 'root', 'root', 'hydee', charset="utf8")  # 服务器名,端口,账户,密码,数据库名

cursor = conn.cursor()
sql = """select a.wareid,warename,waresimname,warespec,a.wareunit,c.classname,prod_add,producer,fileno,barcode
from u_ware_q a,u_ware_ext b ,v_ware_class c 
where a.wareid=b.wareid and a.wareid=c.wareid and c.parentcode='03' """
cursor.execute(sql)
# 如果update/delete/insert记得要conn.commit()
# 否则数据库事务无法提交
# print (cur.fetchall())
# 搜取所有结果
results = cursor.fetchall()

# 获取sqlserver里面的数据字段名称
fields = cursor.description
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)

# 写上字段信息
for field in range(0, len(fields)):
    sheet.write(0, field, fields[field][0])

# 获取并写入数据段信息
row = 1
col = 0
for row in range(1, len(results) + 1):
    for col in range(0, len(fields)):
        sheet.write(row, col, u'%s' % results[row - 1][col])

workbook.save(r'./readout.xlsx')

cursor.close()
# 关闭连接
conn.close()
