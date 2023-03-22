# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/27 16:49
# Desc  : openpyxl库导出Excel 业务数据

# 说明：需要写入的是二维列表target_data
# 将数据写入excel表格

import os
import sys
from datetime import datetime

import openpyxl
import pymssql  # 引入pymssql模块

# 下边链接信息为虚拟的，大家只要对号入座填写自己的数据库连接信息即可
host = 'xxxx'
username = 'root'
passwd = 'root'
db = 'hydee'
port = 3306
charset = "utf8"

current_dir = os.path.dirname(sys.argv[0]) + "\\"
nowDate = datetime.now().strftime('%Y%m%d%H%M%S')

# 获取表头信息
fields = ["门店码(必填)", "商品码(必填)", "最新进价(必填)", "最新售价(必填)", "库存数量(必填)", "销售数量(必填)", "实际销售成本(必填)", "实际销售金额(必填)", "实际销售毛利额(必填)", "首采日期", "引流", "停采"]


def wr_Excel():
    # 连数据库，读取数据
    conn = pymssql.connect('xxxx:11118', 'root', 'root', 'hydee', charset="utf8")
    cur = conn.cursor()
    sql = """SELECT b.busno,a.wareid,a.purprice,saleprice,b.sumqty,sum(c.wareqty),sum(c.netprice),sum(c.purprice),sum(c.netprice)-sum(c.purprice),a.createtime,
    CONVERT(nvarchar(255), CASE WHEN a.purstatus=1  THEN '否' ELSE '是' END),
    CONVERT(nvarchar(255), '否')
    FROM u_ware_q a,u_store_m b ,u_sale_c c 
    WHERE a.wareid=b.wareid AND c.wareid=*b.wareid AND c.busno=*b.busno AND a.wareid=c.wareid
    AND accdate>=convert(nvarchar(10),Dateadd(month,-6,getdate()),23)
    GROUP BY b.busno,a.wareid,a.purprice,saleprice,b.sumqty,a.createtime,a.purstatus
    ORDER BY b.busno """
    cur.execute(sql)
    sql_result = cur.fetchall()
    cur.close()
    conn.close()
    # 写 excel
    book = openpyxl.Workbook()
    sheet = book.active

    sheet.append(fields)
    for i in sql_result:
        # i[10].encode('latin1').decode('cp936')
        # i[11].encode('latin1').decode('cp936')
        # row = list(i)
        # print(row)
        # row[10] = i[10].encode('latin1').decode('cp936')
        # row[11] = i[11].encode('latin1').decode('cp936')
        sheet.append(i)

    save_dir = current_dir + "业务数据_" + "%s.xlsx" % nowDate
    book.save(save_dir)
    print("文件保存: %s", save_dir)


if __name__ == '__main__':
    wr_Excel()
