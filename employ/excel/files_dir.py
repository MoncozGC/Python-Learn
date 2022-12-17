# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/20 9:52
# Desc  : 遍历目录下文件
import os

# 定义读取单个 excel 文件数据
import xlrd


def read_excel(name):
    file_path = path + '/'+ name
    work_book = xlrd.open_workbook(file_path)
    sheet = work_book.sheet_by_index(0)
    return sheet._cell_values[1:]

    # # 测试一下：
    # print(read_excel(files[0]))


if __name__ == '__main__':
    path = './'
    f = os.walk(path)
    files = []

    # os.walk: 目录路径，目录名，文件名
    for dir_path, dir_names, file_names in f:
        for file in file_names:
            # 如果文件类型未.xls格式则输出
            if '2022.xls' in file:
                files.append(file)

    print(files)

    # read_excel(files)
    # print_ts(read_excel(files[1]))

    # 利用列表推导式读取目录下所有数据
    sign_data = [read_excel(name) for name in files]
    # print(sign_data)  # 测试读取到的所有数据

