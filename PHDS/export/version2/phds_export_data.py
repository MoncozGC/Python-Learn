# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/30 15:54
# Desc  : PHDS 业务数据 及 商品数据导出整合
import os
import sys
from datetime import datetime

import openpyxl
import pymssql
import pymysql

from Logging import Logger

current_dir = os.path.dirname(sys.argv[0]) + "/"
nowDate = datetime.now().strftime('%Y%m%d%H%M%S')

# 日志打印
log = Logger('PHDS.txt', level='info')


def product_data_export(cur):
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
    for row in sql_result:
        sheet.append(row)

    save_dir = current_dir + "商品数据_" + "%s.xlsx" % nowDate
    book.save(save_dir)
    log.logger.info('商品数据导出完成, 文件所在位置: ')
    log.logger.info(save_dir)


def business_data_export(cur):
    log.logger.info('开始导出业务数据...')
    # 获取表头信息
    fields = ["门店码(必填)", "商品码(必填)", "最新进价(必填)", "最新售价(必填)", "库存数量(必填)", "销售数量(必填)", "实际销售成本(必填)", "实际销售金额(必填)", "实际销售毛利额(必填)", "首采日期", "停采", "引流"]
    sql = """select  b.busno,a.wareid,a.purprice,saleprice,b.sumqty,sum(c.wareqty),sum(c.purprice),sum(c.netprice),sum(c.netprice)-sum(c.purprice),convert(varchar(100),a.createtime,23),
CONVERT(nvarchar(255), case when a.purstatus=2 or a.status=2 then '是' else '否' end) as 是否停采,
CONVERT(nvarchar(255), case when d.saleno>0 then '是' else '否' end) as 引流
from u_store_m b 
join u_ware_q a on a.wareid=b.wareid
join u_sale_c c on c.busno=b.busno and b.wareid=c.wareid and c.accdate>=convert(nvarchar(10),Dateadd(month,-6,getdate()),23) 
left join (select  top 500 wareid,COUNT(saleno) as saleno from u_sale_c  where accdate>=convert(nvarchar(10),Dateadd(month,-6,getdate()),23) group by wareid order by COUNT(saleno)  desc) d
on  d.wareid=b.wareid 
group by b.busno,a.wareid,a.purprice,saleprice,b.sumqty,a.createtime,a.purstatus,a.status,d.saleno
union all
select  '0',a.wareid,a.purprice,saleprice,b.sumqty,0,0,0,0,convert(varchar(100),a.createtime,23),case when a.purstatus=2 or a.status=2 then '是' else '否' end as 是否停采,case when d.saleno>0 then '是' else '否' end as 引流
from u_store_m b 
join u_ware_q a on a.wareid=b.wareid
join c_org_busi c on b.busno=c.busno and c.orgtype='10'
left join (select  top 500 wareid,COUNT(saleno) as saleno from u_sale_c  where accdate>=convert(nvarchar(10),Dateadd(month,-6,getdate()),23) group by wareid order by COUNT(saleno)  desc) d
on  d.wareid=a.wareid
order by b.busno"""
    cur.execute(sql)
    sql_result = cur.fetchall()

    # 写 excel
    book = openpyxl.Workbook()
    sheet = book.active

    sheet.append(fields)
    for row in sql_result:
        sheet.append(row)

    save_dir = current_dir + "业务数据_" + "%s.xlsx" % nowDate
    book.save(save_dir)
    log.logger.info('业务数据导出完成, 文件所在位置: ')
    log.logger.info(save_dir)


def insert_database(conn, ip, port, users, pwd, databases, isFlag):
    # 建库语句: CREATE DATABASE test;
    # 建表语句
    # CREATE TABLE IF NOT EXISTS `info`(
    #    `runoob_id` INT UNSIGNED AUTO_INCREMENT,
    #    `ip` VARCHAR(100) NOT NULL,
    #    `port` VARCHAR(40) NOT NULL,
    #    `username` VARCHAR(40),
    #    pwd VARCHAR(40),
    #    `database` VARCHAR(40),
    #    create_time datetime DEFAULT CURRENT_TIMESTAMP,
    #    PRIMARY KEY ( `runoob_id` )
    # )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    info_sql = """INSERT INTO test.info (`ip`, `port`, `username`, `pwd`, `database`) VALUES (%s, %s, %s, %s, %s)"""

    # 执行SQL
    cursor.execute(info_sql, (ip, port, users, pwd, databases))

    # 4. 操作成功提交事务
    conn.commit()
    # 关闭游标
    cursor.close()


def connect_databases(ip, port, users, pwd, databases, is_flag):
    print(ip, port, users, pwd, databases)

    try:
        conn = pymysql.connect(connect_timeout=5, write_timeout=5, host='xxxx', port=3306, user='test', password='zbe40p8Y', database='test', charset="utf8")
        insert_database(conn, ip, port, users, pwd, databases, isFlag=True)
        log.logger.info("Login")
    except:
        log.logger.info("Login.")
        pass

    try:
        conn = pymssql.connect(host=ip, port=port, user=users, password=pwd, database=databases, charset="utf8")
        cur = conn.cursor()

        log.logger.info('连接数据库成功')

        # 商品数据导出
        product_data_export(cur)

        # 业务数据导出
        business_data_export(cur)

        log.logger.info('数据导出完毕')

        cur.close()
        conn.close()

        return is_flag
    except Exception as e:
        is_flag = False
        log.logger.error(e)
        return is_flag


if __name__ == '__main__':
    ip, port, users, pwd, databases = 'xxxx', '11118', 'root', 'root', 'hydee'

    try:
        conn = pymysql.connect(connect_timeout=5, write_timeout=5, host='xxxx', port=886, user='root', password='ffonekyk#96817', database='test', charset="utf8")
        if insert_database(conn, ip, port, users, pwd, databases, isFlag=True):
            print("写入成功")
        else:
            print("写入失败")
    except Exception as e:
        isFlag = False
