# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-04-22
# Desc  : oracle导出数据
import cx_Oracle
from tabulate import tabulate


def get_bvt_schema_tables_with_sample(connection_string, schema='BVT'):
    """
    获取指定模式(BVT)下的所有表结构信息和首条数据

    参数:
        connection_string: Oracle连接字符串
        schema: 要查询的模式名称(默认为BVT)

    返回:
        包含表结构信息和首条数据的字典
    """
    connection = cx_Oracle.connect(connection_string)
    cursor = connection.cursor()

    try:
        # 查询BVT模式下的所有表 - 使用替代绑定变量语法
        cursor.execute(f"""
        SELECT TABLE_NAME 
        FROM ALL_TABLES 
        WHERE OWNER = :1 
        ORDER BY TABLE_NAME
        """, [schema.upper()])

        tables = [row[0] for row in cursor]

        # 获取每个表的详细信息
        tables_dict = {}
        for table in tables:
            # 获取表结构信息 - 使用位置绑定变量
            cursor.execute(f"""
            SELECT 
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
                t.OWNER = :1
                AND t.TABLE_NAME = :2
            ORDER BY 
                t.COLUMN_ID
            """, [schema.upper(), table])

            columns = []
            column_names = []
            for row in cursor:
                column_name, data_type, data_length, data_precision, data_scale, nullable, column_id, comments = row

                full_data_type = data_type
                if data_type in ('NUMBER', 'FLOAT'):
                    if data_precision and data_scale:
                        full_data_type = f"{data_type}({data_precision},{data_scale})"
                    elif data_precision:
                        full_data_type = f"{data_type}({data_precision})"
                elif data_type in ('VARCHAR2', 'CHAR', 'NVARCHAR2', 'NCHAR'):
                    full_data_type = f"{data_type}({data_length})"

                columns.append({
                    '字段名': column_name,
                    '字段类型': full_data_type,
                    '是否可为空': nullable,
                    '字段描述': comments if comments else '暂无描述',
                    '字段顺序': column_id
                })
                column_names.append(column_name)

            # 获取表的第一条数据
            sample_data = None
            try:
                if column_names:  # 确保有列名
                    # 使用字符串格式化构建查询，注意SQL注入风险
                    # 因为列名和表名是我们自己从系统表获取的，所以相对安全
                    query = f"SELECT {', '.join(column_names)} FROM {schema}.{table} WHERE ROWNUM = 1"
                    cursor.execute(query)
                    row = cursor.fetchone()
                    if row:
                        sample_data = dict(zip(column_names, row))
            except cx_Oracle.DatabaseError as e:
                sample_data = f"查询数据时出错: {str(e)}"

            tables_dict[table] = {
                'columns': columns,
                'sample_data': sample_data if sample_data else "表中无数据"
            }

        return tables_dict

    finally:
        cursor.close()
        connection.close()


def generate_enhanced_markdown(tables_dict, schema='BVT', output_file=None):
    """
    生成增强版Markdown报告，包含表结构和首条数据

    参数:
        tables_dict: 表结构字典
        schema: 模式名称
        output_file: 输出文件路径(可选)
    """
    report = f"# Oracle数据库数据字典 - 模式: {schema}\n\n"

    for table_name, table_info in tables_dict.items():
        report += f"## 表: {schema}.{table_name}\n\n"

        # 输出表结构
        report += "### 表结构\n\n"
        table_data = []
        for col in table_info['columns']:
            table_data.append([
                col['字段名'],
                col['字段类型'],
                '是' if col['是否可为空'] == 'Y' else '否',
                col['字段描述']
            ])

        report += tabulate(
            table_data,
            headers=['字段名', '字段类型', '可为空', '描述'],
            tablefmt='pipe'
        )
        report += "\n\n"

        # 输出首条数据
        report += "### 首条数据示例\n\n"
        if isinstance(table_info['sample_data'], dict):
            sample_table = []
            for col_name, value in table_info['sample_data'].items():
                sample_table.append([
                    col_name,
                    str(value) if value is not None else "NULL"
                ])
            report += tabulate(
                sample_table,
                headers=['字段名', '值'],
                tablefmt='pipe'
            )
        else:
            report += table_info['sample_data']
        report += "\n\n"

    # 输出到文件或控制台
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"增强版数据字典已生成到: {output_file}")
    else:
        print(report)


if __name__ == "__main__":
    # 配置数据库连接信息
    connection_string = "system/oracle@localhost:1521/ORCL"

    # 获取BVT模式下的表结构和数据
    bvt_tables = get_bvt_schema_tables_with_sample(connection_string, schema='BVT')

    # 生成增强版Markdown报告
    generate_enhanced_markdown(bvt_tables, schema='BVT', output_file="BVT_schema_dictionary_with_samples.md")