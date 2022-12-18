"""
encoding: utf-8
Author: MoncozGC
Date  : 2022/1/4 16:32
Desc  : PHDS 使用SQL查询数据测试
"""
import pymysql

connect = pymysql.connect(host="xxxx", user="root", password="root", port=3306,
                          db="phds_base")
# 创建一个游标对象:有两种创建方法
cursor = connect.cursor()

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
        WHERE dgp.OID = '1632794744960000'
"""

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
print(lines)
print(lines[0][0], lines[0][1], lines[0][2], lines[0][3], lines[0][4],
      lines[0][5], lines[0][6], lines[0][7], lines[0][8], lines[0][9])
# 关闭游标连接
cursor.close()
# 关闭数据库连接
connect.close()
