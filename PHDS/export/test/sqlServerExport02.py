# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/24 21:35
# Desc  : https://www.programminghunter.com/article/461463663/

import pandas as pd
import pymssql

conn = pymssql.connect('xxxx:11118', 'root', 'root', 'hydee')
sql = "select * from Chat_Messages"
df = pd.read_sql(sql, conn)
df['wind'] = (df.symbol + '.' + df.exchange.apply(lambda x: x[-2:]))
print(df)
df.to_excel('sql.xlsx', index=0)
print('ok')
conn.close()
