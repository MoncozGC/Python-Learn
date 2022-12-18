# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/7 21:00
# Desc  : 获取数据库通用名, 根据通用名去噪
if __name__ == '__main__':
    import pymysql

    # connect = pymysql.connect(host="220.168.73.85", user="root", password="Admin@123456", port=8482,
    #                           db="phds_base")
    connect = pymysql.connect(host="xxxx", user="root", password="root", port=3306,
                              db="phds_base")

    sql = """
    SELECT spuName  
FROM td_company_product_sku tcps 
WHERE spuName  REGEXP'[^[:alnum:]]'
    """

    cursor = connect.cursor()

    execute = cursor.execute(sql)

    # 获取全部数据
    lines = cursor.fetchall()

    for it in lines:
        s = "".join(it)
        strip = s.strip("-_ &/*+.、#★？！")
        rstrip = strip.rstrip("-_ &/*+.、#★？！")
        print("原始: %s , 去噪: %s" % (s, rstrip))

    # for it in list(lines):
    #     strip = str(it).strip("-_ &/*+.、#★")
    #     print(strip)
    # rstrip = strip.rstrip("-_ &/*+.、#★")
