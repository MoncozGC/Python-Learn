# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/7/27 16:22
# Desc  : 数据清洗
from utils.comm_util import *

if __name__ == '__main__':
    # 加载配置文件
    from utils.connect_databases import load_config

    appRootDir, config = load_config('Python-Employ', ' ')
    print(appRootDir)

    # 初始化数据库
    from utils.connect_databases import load_database_config

    load_database_config(config)
    from utils.connect_databases import getDatabaseOperation

    sql1 = """ SELECT customer_bizscope FROM org_customer_nmpa LIMIT 10"""

    line = getDatabaseOperation("bhds_base").query(sql1)
    # print(line)

    # 每行数据去除首位特殊符号
    i = 0

    for data in line:
        str_line = str(line[i]).strip(r"~·！!@#￥$%…^&*_-—=+|、\:;\"',./，。：；“”‘？★()")
        i = i + 1
        print_ts(i, str_line)
