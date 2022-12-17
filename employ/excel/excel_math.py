# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/20 13:38
# Desc  : 操作数据文件
import numpy as np
import pandas as pd
import xlrd

from utils.comm_util import print_ts

if __name__ == '__main__':
    open_workbook = xlrd.open_workbook('datas/2022.xls')
    # sheet页
    sheet = open_workbook.sheet_by_index(2)
    # 按行读取表格数据, 从第三行开始读取
    all_data = sheet._cell_values[1:]

    # for ds in all_data:
    #     print_ts(ds)

    total_row = len(all_data)
    print_ts("总行数: ", total_row)

    total_score = sum([int(ds[10]) for ds in all_data])
    print_ts("总分: ", total_score)

    total_avg = round(total_score / total_row, 2)
    print_ts("平均分: ", total_avg)

    # 获取学生姓名一栏
    students = ([ds[2] for ds in all_data])
    students_manages = {key: [0, 0, 0, 0] for key in students}
    # 将学生对应的分数存储起来
    for ds in all_data:
        if ds[2] in students_manages.keys():
            students_manages[ds[2]][0] += int(ds[10])

    max_score = max([int(ds[10]) for ds in all_data])
    # 排除成绩为0的数据, 可能是没有考试 or 没有录入成绩
    min_score = min([int(ds[10]) for ds in all_data if ds[10] != 0])
    print_ts("成绩[最高分\最低分]: ", max_score, min_score)

    max_stu = [key for key in students_manages.keys()
               if students_manages[key][0] == max_score]
    min_stu = [key for key in students_manages.keys()
               if students_manages[key][0] == min_score]

    print_ts("姓名[最高分\最低分]: ", max_stu, min_stu)


