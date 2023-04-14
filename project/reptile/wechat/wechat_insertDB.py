"""
encoding: utf-8
Author: MoncozGC
Date  : 2022/1/3 22:38
Desc  : 将生成微信聊天记录TXT文本, 写入到数据库中
"""
import re

import pymysql

# conn = pymysql.connect(
#     host='xxxxx',
#     user='root',
#     password='root',
#     db='test',
#     charset='utf8mb4',
#     port=3306)

conn = pymysql.connect(
    host='192.168.153.161',
    user='ambari',
    password='ambari',
    db='test',
    charset='utf8mb4',
    port=3306)

cur = conn.cursor()

with open(r"../datas/小妞儿.txt", encoding='utf-8') as f:
    lines = f.readlines()
    filter_lines = []
    reg = "^.+[\u4E00-\u9FFF]\s\(.+\):"
    # reg = "^.*\s\(.+\):"

    for line in lines:
        # 去除转发的聊天记录 简单过滤
        if (line.startswith('机器') or line.startswith('小妞儿')) and re.match(reg, line):
            filter_lines.append(line.strip())
    # count = 0
for line in filter_lines:
    s1 = line.find(" ")
    s2 = line.find("):")
    name = line[:s1]
    time = line[s1 + 2:s2]
    content = line[s2 + 2:]
    print(line)
    # if count > 1000:
    #     break
    # else:
    insert_sql = f"insert into log(user,datetime,content) values ('{name}','{time}' ,'{pymysql.escape_string(content)}')"
    cur.execute(insert_sql)
conn.commit()
