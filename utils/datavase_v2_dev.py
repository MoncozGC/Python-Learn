# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/30 16:00
# Desc  :
import pandas as pd
from connect_databases_v2 import DBConnCls

# 假设您的配置文件是一个字典，如下所示：
conf = {
    "mysql": {
        "host": "server01",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "dev"
    }
}

# 创建一个简单的 DataFrame
data = {'id': [1, 2, 3], 'email': ['A', 'B', 'C'], 'password': ['1', '2', '3'], 'username': ['a', 'b', 'c']}
df = pd.DataFrame(data)

# 使用工具类将 DataFrame 写入 MySQL 数据库
db_conn = DBConnCls(conf)
db_conn.write_df_to_sql(df, 'user', if_exists='append')
