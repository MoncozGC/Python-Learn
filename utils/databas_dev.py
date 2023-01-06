# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/7/27 16:55
# Desc  : 数据库工具类测试


if __name__ == '__main__':
    # 加载配置文件
    # from utils.connect_databases import load_config
    #
    # appRootDir, config = load_config('Python-Learn', ' ')
    #
    # # 初始化数据库
    # from utils.connect_databases import load_database_config
    #
    # load_database_config(config)
    from utils.connect_databases import getDatabaseOperation

    sql1 = """ SELECT * FROM weather LIMIT 1"""

    query = getDatabaseOperation("world").query(sql1)
    print(query)

    sql2 = """ SELECT * FROM ads_id_odr_details_out_1d LIMIT 1"""

    query2 = getDatabaseOperation("bhds_bi").query(sql2)
    print(query2)
