# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-04-21
# Desc  :

# 数据库配置
import mysql.connector

db_config = {
    'user': 'root',
    'password': 'hadoop',
    'host': 'localhost',
    'database': 'moncozgc'
}


# 创建数据库连接
def create_connection():
    return mysql.connector.connect(**db_config)


def init_connection():
    conn = create_connection()
    cursor = conn.cursor()
    return conn, cursor


def execute_one(sql, params):
    """
    执行带参数的sql
    """
    conn, cursor = init_connection()

    try:
        cursor.execute(sql, params)
        conn.commit()
    except mysql.connector.Error as err:
        print('执行错误\nSQL: %s\nERROR: %s' % (sql, err))
    finally:
        cursor.close()
        conn.close()


def execute_list(sql, param_list):
    """
    执行批量插入
    :param sql: SQL 插入语句
    :param param_list: 参数列表，每个元素是一个包含行数据的元组
    """
    conn, cursor = init_connection()

    try:
        cursor.executemany(sql, param_list)
        conn.commit()
        print(f"成功插入{cursor.rowcount}条数据。")
    except mysql.connector.Error as err:
        print('执行错误\nSQL: %s\nERROR: %s' % (sql, err))
    finally:
        cursor.close()
        conn.close()


# 查询数据
def query_data(sql):
    conn, cursor = init_connection()

    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print('查询错误\nSQL: %s\nERROR: %s' % (sql, err))
    finally:
        cursor.close()
        conn.close()


def begin_transaction():
    """开始事务"""
    conn, cursor = init_connection()

    cursor.execute("START TRANSACTION")


def commit():
    """提交事务"""
    conn, cursor = init_connection()

    cursor.execute("COMMIT")


def rollback():
    """回滚事务"""
    conn, cursor = init_connection()
    cursor.execute("ROLLBACK")


def get_last_insert_id():
    """获取最后插入ID"""
    conn, cursor = init_connection()

    cursor.execute("SELECT LAST_INSERT_ID()")
    return cursor.fetchone()[0]
