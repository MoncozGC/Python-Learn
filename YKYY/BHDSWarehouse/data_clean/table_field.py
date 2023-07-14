# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023-07-14
# Desc  : 读取数据库表字段名及字段类型, 将其转化为字典类型数据, 在转换为dataframe
# 场景: 当FlinkCDC监控表数据, 发送binlog json数据至kafka时, 如果有字段再表设计时是可以为null的, 并且实际该字段为null, 那么这个字段就不会监控到
# 而这样的做法是为了初始化好dataframe的结构, 如果少了字段则填补.
import pymysql

from utils.comm_util import print_ts

table_name = 'stg_spr_gdsbs'

if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.153.140', user='root', port=3306, password='hadoop', db='bdcp_stg')
    cursor = conn.cursor()

    # 执行查询字段名和字段类型的语句
    query = f"SHOW COLUMNS FROM {table_name}"
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    data, num = '', 0
    field = ['emp_oid', 'crt', 'upt', 'cstatus']
    for row in result:
        column_name = row[0]
        column_type = row[1]
        if column_name in field: continue
        num += 1
        data += column_name + " " + column_type.replace(' unsigned', '') + '\n'

    print_ts(data, num, '\n')

    # 关闭连接
    cursor.close()
    conn.close()

    converted_data, not_mapping = {}, []
    lines = data.split('\n')
    for line in lines:
        if line.strip() != '':
            key, value = line.split()
            if 'bigint' in value or 'smallint' in value or 'int' in value or 'tinyint' in value:
                converted_data[key] = 0
            elif 'varchar' in value or 'json' in value or 'text' in value or 'char' in value:
                converted_data[key] = ''
            else:
                not_mapping.append(key)

    print_ts(converted_data, '\n', len(converted_data))
    print_ts("有效字段数量: %s, 格式化后有效字段数量: %s " % (num, len(converted_data)))
    print_ts('丢失字段:', not_mapping)

"""
def dataframe_normalization(data: DataFrame = None, struct: str = None):
    标准化表结构
    :param data:
    :param struct: 标准化数据结构 在配置文件中的 key
    :return:
    
    fields = []
    if struct is not None:
        ext = CnfUtil.cnf['init_table'][struct]
        fields.append(ext)
    if data is not None:
        columns = data.columns
        for ds in fields:
            for key, value in eval(ds).items():
                if key not in columns:
                    data[key] = value
    return data
"""
