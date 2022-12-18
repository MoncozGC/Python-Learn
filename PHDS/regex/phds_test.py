"""
encoding: utf-8
Author: MoncozGC
Date  : 2021/12/29 13:12
Desc  :  测试方法
"""
import datetime
from clickhouse_driver import Client
import pymysql
import pprint

ckClient = Client(host='xxxx', database='bds_dw', user='default', password='default')

# 返回当前时间 yyyy-MM-dd hh:MM:ss
match_time = '2018-05-22 08:30:00'
ctime = datetime.datetime.now()
print("当前时间: %s" % ctime)


def mysql_data_get(sql):
    # 连接数据库
    connect = pymysql.connect(host="xxxx", user="root", password="root", port=3306,
                              db="phds_base")
    # 创建一个游标对象:有两种创建方法
    cursor = connect.cursor()
    # 使用游标的execute()方法执行sql语句
    execute = cursor.execute(sql)

    # print(execute)
    # print(lines[2][0], lines[2][1], lines[2][2], lines[2][3], lines[2][4],
    #       lines[2][5], lines[2][6], lines[2][7], lines[2][8], lines[2][9])
    #
    # print(lines[0][0], lines[0][1], lines[0][2], lines[0][3], lines[0][4],
    #       lines[0][5], lines[0][6], lines[0][7], lines[0][8], lines[0][9])

    # 获取全部数据
    lines = cursor.fetchall()
    # 关闭游标连接
    cursor.close()
    # 关闭数据库连接
    connect.close()

    return execute


def change_diagnose_status(remarks):
    """
    测试 更改诊断状态
    :param remarks:
    :return:
    """
    a = 0
    if remarks is None or remarks == '':
        a = 0
    else:
        if len(remarks) > 24:
            remarks = remarks[:24]
        a = 1
    return a


if __name__ == '__main__':
    # print(change_diagnose_status("数据不匹配或业务数据不存在"))
    # print(len("数据不匹配或业务数据不存在"))

    # if len(lines) == 1:
    #     raise ValueError('诊断流程任务查询失败')

    # 创建诊断任务
    # create_diagnose_process_task_sql = """
    # SELECT OID,spuName,IFNULL(skuName,''),IFNULL(stdCode,'0'),IFNULL(apprNum,'0'),IFNULL(dosForm,''),IFNULL(manuFac,''),IFNULL(orgPlace,''),IFNULL(specStr,''),IFNULL(packUnit,''),matchMode FROM td_company_product_sku WHERE matchStatus=0"""
    # create_diagnose_process_task = mysql_data_get(create_diagnose_process_task_sql)
    # print(create_diagnose_process_task)

    sql = """
    SELECT 
            dgp.compGroupOID, dgp.diagType, 
            DATEDIFF(dgp.dataRangeEnd,dgp.dataRangeStart)+1,
            dgp.diagStatus,dgp.diagCfyArr,
            c.compGroupName,c.compGroupType,
            dgp.hangup,cc.marketLv,
            CONCAT(dgp.dataRangeStart,'- ',dgp.dataRangeEnd) 
            FROM td_company_diagnose_proc dgp 
            INNER JOIN tb_company_group c ON c.OID = dgp.compGroupOID
            INNER JOIN tb_company_all cc ON cc.OID = dgp.compOID
            where dgp.OID = '1632794744960000';
    """
    task = mysql_data_get(sql)
    print(task)

