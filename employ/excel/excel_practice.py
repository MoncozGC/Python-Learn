# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/18 10:37
# Desc  :
import xlrd

from utils.comm_util import print_ts

if __name__ == '__main__':
    work_book = xlrd.open_workbook('datas/2022.xlsx')

    # 输出sheet页
    print_ts("sheet页数: ", work_book.nsheets)

    sheets = work_book.sheets()
    print_ts("获取工作薄中所有sheet表对象: ", sheets)

    sheet_names = work_book.sheet_names()
    print_ts("获取sheet页名称: ", sheet_names)

    sheet_1 = work_book.sheet_by_index(0)
    print_ts("按索引获取sheet对象: ", sheet_1)

    sheet_2 = work_book.sheet_by_name("Sheet2")
    print_ts("按sheet表名称获取sheet对象，名称分大小写: ", sheet_2)

    cell_2 = sheet_2.cell(0, 0)
    print_ts("获取sheet表单元格对象: ", cell_2)

    cell_2_value = sheet_2.cell_value(0, 0)
    print_ts("获取sheet表单元格值: ", cell_2_value)

    cell_2_type = sheet_2.cell_type(0, 0)
    print_ts("获取单元格类型: ", cell_2_type)

    row_sum = sheet_2.nrows
    print_ts("有效行数: ", row_sum)

    row_len = sheet_2.row_len(0)
    print_ts("获取sheet表某一行长度", row_len)

    row_0 = sheet_2.row(0)
    print_ts("获取第一行所有数据类型及值", row_0)

    # row_slice(第几行开始, 开始于第几列, 结束于第几列)
    row_0_slice = sheet_2.row_slice(0, 0, row_len)
    print_ts(row_0_slice)

    row_0_type = sheet_2.row_types(0)
    print_ts("获取sheet表对象某一行数据类型,返回一个数组对象: ", row_0_type)

    # row_values(第几行开始, 开始于第几列, 结束于第几列)
    row_0_value = sheet_2.row_values(0, 0, 3)
    print_ts("获取sheet表对象某一行数据值", row_0_value)

    # rows = sheet_2.get_rows()
    # print_ts("获得sheet对象所有行对象生成器: ", rows)

    # 获取sheet表所有行 打印的地址值
    # for row in rows:
    #     print_ts(rows)

    col_sum = sheet_2.ncols
    print_ts("获取有效列数: ", col_sum)

    col_0 = sheet_2.col_slice(1)
    print_ts("获取某一列的值: ", col_0)

    col_0_type = sheet_2.col_types(0)
    print_ts("获取某一列的数据类型: ", col_0_type)

    data_row = []
    for row in range(sheet_2.nrows):
        data_row.append(sheet_2.row_values(row))

    print_ts("按行读取数据: ", data_row)

    for col in range(sheet_2.ncols):
        data_cel = sheet_2.col_values(col)

    # print_ts(data_cel)

    data_col = [sheet_2.col_values(i) for i in range(sheet_2.ncols)]
    print("按列读取数据: ", data_col)

    # 按行读取test01.xls 所有 sheet 表数据
    all_data = {}
    for i, sheet_obj in enumerate(work_book.sheets()):
        all_data[i] = [sheet_obj.row_values(row)
                       for row in range(sheet_obj.nrows)]

    print_ts(all_data)
