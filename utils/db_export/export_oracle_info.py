# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-04-22
# Desc  : oracle导出数据
import cx_Oracle
from tabulate import tabulate


def get_oracle_tables_dict(connection_string, schema=None, table_name=None):
    """
    获取Oracle表结构并生成数据字典

    参数:
        connection_string: Oracle连接字符串(如: username/password@host:port/service_name)
        schema: 指定的模式/用户名(可选)
        table_name: 指定的表名(可选)

    返回:
        包含表结构信息的字典
    """
    # 连接Oracle数据库
    connection = cx_Oracle.connect(connection_string)
    cursor = connection.cursor()

    try:
        # 构建查询SQL
        sql = """
        SELECT 
            t.TABLE_NAME,
            t.COLUMN_NAME,
            t.DATA_TYPE,
            t.DATA_LENGTH,
            t.DATA_PRECISION,
            t.DATA_SCALE,
            t.NULLABLE,
            t.COLUMN_ID,
            c.COMMENTS
        FROM 
            ALL_TAB_COLUMNS t
        LEFT JOIN 
            ALL_COL_COMMENTS c ON t.TABLE_NAME = c.TABLE_NAME 
            AND t.COLUMN_NAME = c.COLUMN_NAME 
            AND t.OWNER = c.OWNER
        WHERE 
            t.OWNER = NVL(:schema, t.OWNER)
            AND t.TABLE_NAME = NVL(:table_name, t.TABLE_NAME)
        ORDER BY 
            t.TABLE_NAME, t.COLUMN_ID
        """

        # 执行查询
        cursor.execute(sql, {'schema': schema.upper() if schema else None,
                             'table_name': table_name.upper() if table_name else None})

        # 处理结果
        tables_dict = {}
        for row in cursor:
            table_name = row[0]
            column_name = row[1]
            data_type = row[2]
            data_length = row[3]
            data_precision = row[4]
            data_scale = row[5]
            nullable = row[6]
            column_id = row[7]
            comments = row[8]

            # 构建完整数据类型(处理NUMBER/VARCHAR2等)
            full_data_type = data_type
            if data_type in ('NUMBER', 'FLOAT'):
                if data_precision and data_scale:
                    full_data_type = f"{data_type}({data_precision},{data_scale})"
                elif data_precision:
                    full_data_type = f"{data_type}({data_precision})"
            elif data_type in ('VARCHAR2', 'CHAR', 'NVARCHAR2', 'NCHAR'):
                full_data_type = f"{data_type}({data_length})"

            # 添加到字典
            if table_name not in tables_dict:
                tables_dict[table_name] = []

            tables_dict[table_name].append({
                '字段名': column_name,
                '字段类型': full_data_type,
                '是否可为空': nullable,
                '字段描述': comments if comments else '暂无描述',
                '字段顺序': column_id
            })

        return tables_dict

    finally:
        cursor.close()
        connection.close()


def get_oracle_vies_sql(connection_string, schema, output_file=None):
    # 连接Oracle数据库
    connection = cx_Oracle.connect(connection_string)
    cursor = connection.cursor()

    try:
        SQL = """SELECT VIEW_NAME, TEXT FROM ALL_VIEWS WHERE OWNER = NVL(:schema, OWNER) """
        cursor.execute(SQL, {schema: schema.upper() if schema else None})

        report = "# Oracle数据库视图SQL\n\n"
        for row in cursor:
            report += f"## 视图名称: {row[0]}\n\n```sql\n{row[1]}\n```\n\n"

        # 输出到文件或控制台
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"数据视图已生成到: {output_file}")
        else:
            print(report)
    finally:
        cursor.close()
        connection.close()


def generate_markdown_report(tables_dict, output_file=None):
    """
    生成Markdown格式的数据字典报告

    参数:
        tables_dict: 表结构字典
        output_file: 输出文件路径(可选)
    """
    report = "# Oracle数据库表结构数据字典\n\n"

    for table_name, columns in tables_dict.items():
        report += f"## 表名: {table_name}\n\n"

        # 准备表格数据
        table_data = []
        for col in columns:
            table_data.append([
                col['字段名'],
                col['字段类型'],
                col['是否可为空'],
                col['字段描述']
            ])

        # 使用tabulate生成Markdown表格
        report += tabulate(
            table_data,
            headers=['字段名', '字段类型', '是否可为空', '字段描述'],
            tablefmt='pipe'
        )
        report += "\n\n"

    # 输出到文件或控制台
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"数据字典已生成到: {output_file}")
    else:
        print(report)


if __name__ == "__main__":
    # 配置数据库连接信息
    connection_string = "system/oracle@localhost:1521/ORCL"

    print("开始执行")
    # 可选: 指定特定schema和表名
    schema = "BVT1"
    # table_name = "EMP"

    # 获取表结构
    tables_dict = get_oracle_tables_dict(connection_string, schema)  # 可传入schema和table_name参数

    # 生成Markdown报告
    generate_markdown_report(tables_dict, output_file="oracle_data_dictionary.md")

    # 获取视图MD报告
    get_oracle_vies_sql(connection_string, schema, output_file="oracle_data_views.md")
