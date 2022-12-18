# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/30 15:54
# Desc  : PHDS 业务数据 及 商品数据导出整合
import os
import sys
from datetime import datetime

import openpyxl
import pymssql

from utils.Logging import Logger

current_dir = os.path.dirname(sys.argv[0]) + "/"
nowDate = datetime.now().strftime('%Y%m%d%H%M%S')

# 日志打印
log = Logger('PHDS.log', level='info')


def business_data_export():
    log.logger.info('开始导出业务数据...')
    # 获取表头信息
    fields = ["门店码(必填)", "商品码(必填)", "最新进价(必填)", "最新售价(必填)", "库存数量(必填)", "销售数量(必填)", "实际销售成本(必填)", "实际销售金额(必填)", "实际销售毛利额(必填)", "首采日期", "引流", "停采"]
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

    # 写 excel
    book = openpyxl.Workbook()
    sheet = book.active

    sheet.append(fields)
    for i in sql_result:
        sheet.append(i)

    save_dir = current_dir + "业务数据_" + "%s.xlsx" % nowDate
    book.save(save_dir)
    log.logger.info(save_dir)


def product_data_export():
    log.logger.info('开始导出商品数据...')
    # 表头
    fields = ["商品码(必填)", "通用名(必填)", "商品名", "商品规格(必填)", "包装单位(必填)", "剂型(必填)", "产地", "生产厂家(必填)", "批准文号(必填)", "国际标准码(必填)"]

    sql = """SELECT 
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
    FROM u_ware_q a,u_ware_ext b ,v_ware_class c 
    WHERE a.wareid=b.wareid AND a.wareid=c.wareid AND c.parentcode='03' """

    cur.execute(sql)
    sql_result = cur.fetchall()

    # 写 excel
    book = openpyxl.Workbook()
    sheet = book.active

    sheet.append(fields)
    for i in sql_result:
        row = list(i)
        sheet.append(row)
    save_dir = current_dir + "商品数据_" + "%s.xlsx" % nowDate
    book.save(save_dir)
    log.logger.info(save_dir)


if __name__ == '__main__':
    # bat执行脚本
    for s in range(1, len(sys.argv)):
        # 对参数进行处理
        print("参数{0}为：{1}".format(s, sys.argv[s]))

    log.logger.info('开始导出数据, 请稍等...')
    # 连数据库，读取数据
    conn = pymssql.connect('xxxx:11118', 'root', 'root', 'hydee', charset="utf8")

    # BAT文件输入
    # ip = sys.argv[1]
    # port = sys.argv[2]
    # users = sys.argv[3]
    # pwd = sys.argv[4]
    # databases = sys.argv[5]
    # conn = pymssql.connect(host=ip, port=port, user=users, password=pwd, database=databases, charset="utf8")

    cur = conn.cursor()

    # 商品数据导出
    product_data_export()

    # 业务数据导出
    business_data_export()

    cur.close()
    conn.close()

    # 打包使用
    input('Press Enter to exit…')
