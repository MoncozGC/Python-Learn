# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-03-04
# Desc  : 导出数据库信息(元数据信息、数据库表信息、创建语句)
import os

import pymysql
from pymysql.cursors import Cursor


def export_db_information_schema(cursor: Cursor):
    """
    导出mysql数据库中的 information_schema, 包含了数据库中的元数据信息

    :param cursor: 数据库链接信息
    """
    info_file = "./data/information_schema.sql"
    # 创建 SQL 文件
    with open(info_file, "w", encoding="utf-8") as f:

        # 1. 导出数据库信息（SCHEMATA）
        f.write("-- INSERT INTO `databases` 表示数据库信息\n")
        cursor.execute("SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM SCHEMATA")
        for row in cursor.fetchall():
            f.write(f"INSERT INTO databases (name, charset, collation) VALUES ('{row[0]}', '{row[1]}', '{row[2]}');\n")
        f.write("\n")

        # 2. 导出表信息（TABLES）
        f.write("-- INSERT INTO `tables` 表示所有表的信息\n")
        cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME, ENGINE, TABLE_ROWS, TABLE_COMMENT FROM TABLES")
        for row in cursor.fetchall():
            f.write(f"INSERT INTO tables (db_name, table_name, engine, table_rows, comment) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', {row[3]}, '{row[4]}');\n")
        f.write("\n")

        # 3. 导出字段信息（COLUMNS）
        f.write("-- INSERT INTO `columns` 表示所有字段的信息\n")
        cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT FROM COLUMNS")
        for row in cursor.fetchall():
            column_default = f"'{row[6]}'" if row[6] is not None else "NULL"
            f.write(
                f"INSERT INTO columns (db_name, table_name, column_name, position, column_type, nullable, default_value, comment) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', {row[3]}, '{row[4]}', '{row[5]}', {column_default}, '{row[7]}');\n")
        f.write("\n")

        # 4. 导出索引信息（STATISTICS）
        f.write("-- INSERT INTO `indexes` 表示所有索引的信息\n")
        cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, NON_UNIQUE FROM STATISTICS")
        for row in cursor.fetchall():
            f.write(f"INSERT INTO indexes (db_name, table_name, index_name, column_name, is_unique) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {0 if row[4] == 0 else 1});\n")
        f.write("\n")

        # 5. 导出主键/外键信息（KEY_COLUMN_USAGE）
        f.write("-- INSERT INTO `constraints` 表示主键和外键信息\n")
        cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM KEY_COLUMN_USAGE")
        for row in cursor.fetchall():
            referenced_table = f"'{row[4]}'" if row[4] is not None else "NULL"
            referenced_column = f"'{row[5]}'" if row[5] is not None else "NULL"
            f.write(
                f"INSERT INTO constraints (db_name, table_name, column_name, constraint_name, referenced_table, referenced_column) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {referenced_table}, {referenced_column});\n")
        f.write("\n")

        # 6. 导出视图信息（VIEWS）
        f.write("-- INSERT INTO `views` 表示所有视图的信息\n")
        cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME, VIEW_DEFINITION FROM VIEWS")
        for row in cursor.fetchall():
            view_definition = row[2].replace("'", "''")  # 处理 SQL 语句中的单引号
            f.write(f"INSERT INTO views (db_name, view_name, definition) VALUES ('{row[0]}', '{row[1]}', '{view_definition}');\n")

    print(f"SQL 插入语句文件已生成: {info_file}")


def export_db_table_desc(cursor: Cursor):
    """
    导出数据库中所有表的表结构及视图定义

    :param cursor: 数据库链接
    """
    # 查询所有数据库
    cursor.execute("SHOW DATABASES")
    databases = [row[0] for row in cursor.fetchall()]

    # 处理每个数据库
    for db in databases:
        if db in ['information_schema', 'mysql', 'performance_schema']:  # 排除系统库
            continue

        info_file = f'./data/{db}_INFO.md'
        # 创建每个数据库的 Markdown 文件
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"# `{db}` 库的表结构和视图定义\n\n")

            # 1. 导出所有表的结构
            f.write("## 表结构\n\n")

            # 查询当前数据库下的所有表以及表注释
            cursor.execute(f"""SELECT TABLE_NAME, TABLE_COMMENT FROM information_schema.tables WHERE TABLE_SCHEMA='{db}'""")
            tables = cursor.fetchall()

            for table, table_comment in tables:
                f.write(f"### {table}\n\n")

                # 如果表有注释，添加到 Markdown 中
                if table_comment:
                    f.write(f"> 表注释: {table_comment}\n\n")

                f.write("| 序号 | 字段名 | 字段类型 | 字段备注 |\n")
                f.write("|----|----|----|----|\n")

                # 获取表的字段信息
                cursor.execute(f"""SELECT ORDINAL_POSITION, COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT FROM information_schema.columns WHERE TABLE_SCHEMA='{db}' AND TABLE_NAME='{table}' ORDER BY ORDINAL_POSITION""")

                for row in cursor.fetchall():
                    f.write(f"| {row[0]} | {row[1]} | {row[2]} | {row[3] if row[3] else ''} |\n")

                f.write("\n")

            # 2. 导出所有视图的创建 SQL
            f.write("## 视图创建 SQL\n\n")

            # 查询当前数据库下的所有视图
            cursor.execute(f"SELECT TABLE_NAME FROM information_schema.views WHERE TABLE_SCHEMA='{db}'")
            views = [row[0] for row in cursor.fetchall()]

            for view in views:
                f.write(f"### {view}\n\n")

                # 获取视图的创建 SQL
                cursor.execute(f"SHOW CREATE VIEW {db}.{view}")
                create_view_sql = cursor.fetchone()[1]  # 获取视图的创建 SQL

                f.write(f"```sql\n{create_view_sql}\n```\n\n")

        print(f"Markdown 文件已生成: {info_file}")

        # 3. 导出所有表的 CREATE TABLE 语句
        ddl_file = f"./data/{db}_DDL.md"
        with open(ddl_file, "w", encoding="utf-8") as f_create:
            f_create.write(f"# `{db}` 库的创建表语句\n\n")

            for table, _ in tables:
                f_create.write(f"### {table}\n\n")

                # 获取 CREATE TABLE 语句
                cursor.execute(f"SHOW CREATE TABLE {db}.{table}")
                create_table_sql = cursor.fetchone()[1]  # 获取创建表的 SQL

                f_create.write(f"```sql\n{create_table_sql}\n```\n\n")

        print(f"DLL语句文件已生成: {ddl_file}")


def main_run():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='hadoop',
        database='information_schema',
        charset='utf8'
    )
    cursor = conn.cursor()

    if not os.path.isdir('./data'):
        os.mkdir('./data')

    export_db_information_schema(cursor)
    export_db_table_desc(cursor)

    # 关闭连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main_run()
