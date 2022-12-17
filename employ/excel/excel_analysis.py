# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/20 10:09
# Desc  : 分析2020年江苏省事业单位招聘岗位 Excel 表格信息
# https://blog.csdn.net/zhouz92/article/details/106978058

import xlrd
import xlwt

from utils.comm_util import print_ts


def fill(i, j, data_list):
    """
    向上查找数据函数
    :param i:
    :param j:
    :param data_list:
    :return:
    """
    # 获取上一个的位置数据
    up_index = i - 1
    for c in range(i):
        # 如果上一个位置的数据类容不为空, 则获取返回
        if data_list[up_index][j] != '':
            return data_list[up_index][j]
        else:
            up_index -= 1


if __name__ == '__main__':
    open_workbook = xlrd.open_workbook('datas/sample3.xls')
    # sheet页
    sheet = open_workbook.sheet_by_index(1)
    # 按行读取表格数据, 从第三行开始读取
    all_data = sheet._cell_values[3:]

    # 因为有合并表格, 所以会导致有数据缺失的情况
    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据下标和数据
    # i: 整个数据中的第几条, ds: 对应i条数中的具体数据
    # j: 为对应i条数具体数据中的第几个字段, d: 对应i条数具体数据, 下标为j的字段数据
    """
    eg:  [1.0, '江苏省纪委监委机关', '江苏省廉政信息中心（江苏省廉政电教中心）', 1001.0, '全额拨款', '信息化建设', '001', '管理类', '从事纪检监察信息化建设相关工作', 2.0, '1∶5', '本科及以上', '计算机（大类）类', '不限', '中共党员，取得相应学位，具有两年及以上工作经历', '面试25%，专业测试25%', '需要经常加班、出差；进编', '025-82282281025-82282272（传真）徐剑锋']
    该条数据为读取数据的第一条: i为1, ds为整条数据类容.  j为1时, d为'1.0'; j为2时, d为'江苏省纪委监委机关'...以此类推
    """
    for i, ds in enumerate(all_data):
        for j, d in enumerate(ds):
            if d == '':
                # 将缺失的数据条数下标传递至补全函数中
                ds[j] = fill(i, j, all_data)

    # for ds in all_data:
    #     print_ts(ds)

    # 总招聘岗位数，总招聘人数，岗位最大、最小招聘人数
    total_post = len(all_data)
    print_ts("总招聘岗位数: ", total_post)

    total_employs = sum([int(ds[9]) for ds in all_data])
    print_ts("总招聘岗位: ", total_employs)

    max_employs = max([int(ds[9]) for ds in all_data])
    print_ts("岗位最大招聘人数: ", max_employs)

    min_employs = min([int(ds[9]) for ds in all_data])
    print_ts("岗位最小招聘人数: ", min_employs)

    # 获取有多少招聘个数种类
    number_employs = set([int(ds[9]) for ds in all_data])
    print_ts("招聘种类: ", number_employs)

    # 获取每个招聘数量的岗位数量
    # 建立字典
    ne_dict = {key: 0 for key in number_employs}
    print_ts("建立字典: ", ne_dict)

    for ds in all_data:
        if ds[9] in ne_dict.keys():
            ne_dict[ds[9]] += 1
    print_ts("每个招聘数量的岗位数量: ", ne_dict)

    # 分析招聘对象数据
    # 建立不同招聘对象数量数据
    employ_type = {'社会人员': [0, 0], '应届毕业生': [0, 0], '不限': [0, 0]}

    # 遍历所有招聘信息对应的招聘人数统计至建立的招聘对象数据信息
    for ds in all_data:
        if ds[13] in employ_type.keys():
            employ_type[ds[13]][0] += int(ds[9])

    sum_employ = sum([employ_type['社会人员'][0],
                      employ_type['应届毕业生'][0],
                      employ_type['不限'][0], ])

    for vs in employ_type.values():
        vs[1] = str(round(vs[0] / sum_employ * 100, 2)) + '%'

    print_ts("占比数据: ", employ_type, sum_employ)

    # 专业为计算机相关专业，招聘对象为应届毕业生的所有招聘信息
    s1_data = [data for data in all_data
               if '计算机' in data[12] and data[13] == '应届毕业生']

    for ds in s1_data:
        print_ts(ds)

    s1_post, s1_employs = len(s1_data), sum([int(data[9]) for data in s1_data])

    print_ts("计算机招聘岗位数: ", s1_post, ",计算机招聘人数: ", s1_employs)

    s1_post_ratio, s1_employs_ratio = (round(s1_post / total_post * 100, 2),
                                       round(s1_employs / total_employs * 100, 2))
    print_ts("计算机招聘岗位数占比: ", s1_post_ratio, ",计算机人数在全部招聘信息中占比: ", s1_employs_ratio)

    # 统计学历要求情况: 招聘岗位数, 招聘人数
    s1_academic = {'中专': [0.0, 0.0], '大专': [0.0, 0.0], '本科': [0.0, 0.0],
                   '硕士': [0.0, 0.0], '博士': [0.0, 0.0]}

    for data in s1_data:
        for key in s1_academic.keys():
            if key in data[11]:
                s1_academic[key][0] += 1
                s1_academic[key][1] += int(data[9])

    for value in s1_academic.values():
        value.append(round(value[0] / s1_post * 100, 2))
        value.append(round(value[1] / s1_employs * 100, 2))

    print_ts("学历占比统计情况: ", s1_academic)

    # 统计各主管部门招聘人数，占总招聘人数比例
    # 分析各个主管部门招聘人数
    manages = set([ds[1] for ds in all_data])
    print_ts("统计招聘主管部门: ", manages)

    # 建立主管部门招聘人数数据
    # 值为列表，列表对应的数据为：[招聘人数，占比 % ，社会人员招聘人数，应届毕业生人数，不限人数]
    employ_manages = {key: [0, 0, 0, 0, 0] for key in manages}
    for ds in all_data:
        if ds[1] in employ_manages.keys():
            employ_manages[ds[1]][0] += int(ds[9])

    for key in employ_manages.keys():
        employ_manages[key][1] = round(employ_manages[key][0] / total_employs * 100, 2)

    print_ts("主管部门招聘人数占比: ", employ_manages)

    # 最大\最小招聘人数部门
    max_employ = max([int(employ_manages[key][0]) for key in employ_manages.keys()])
    min_employ = min([int(employ_manages[key][0]) for key in employ_manages.keys()])
    print_ts("最大\最小招聘人数: ", max_employ, min_employ)

    # 查找最大招聘人数、最小招聘人数部门, 可能有多个
    max_manages = [key for key in employ_manages.keys()
                   if employ_manages[key][0] == max_employ]
    min_manages = [key for key in employ_manages.keys()
                   if employ_manages[key][0] == min_employ]
    print_ts("查找最大招聘人数、最小招聘人数部门: ", max_manages, min_manages)

    # 分析每个主管部门招聘对象为：社会人员、应届毕业生、不限 的人数，及其内部比例。
    e_type = ['社会人员', '应届毕业生', '不限']

    for data in all_data:
        for key in employ_manages.keys():
            if key == data[1]:
                for i, type_ in enumerate(e_type):
                    if data[13] == type_:
                        employ_manages[key][2 + i] += int(data[9])

    for value in employ_manages.values():
        for i in range(2, 5):
            value.append(round(value[i] / value[0] * 100, 2))

    print_ts(employ_manages)

    # 保存数据
    # 新建Excel文件、写入数据
    # 整理统计分析数据：基础数据
    info1 = {'总招聘岗位数': total_post,
             '总招聘人数': total_employs,
             '最大招聘人数': max_employ,
             '最小招聘人数': min_employ}

    # 新建Excel表格 写入分析数据：
    new_work = xlwt.Workbook()  # 新建Excel工作簿
    new_sheet = new_work.add_sheet('统计分析数据')  # 创建sheet表
    # 写入数据：
    new_sheet.write_merge(0, 0, 0, 5, '江苏省2020年事业单位招聘岗位表分析结果')
    # 写入基础分析数据
    row_no = 1
    for key, value in info1.items():
        new_sheet.write(row_no, 0, key)
        new_sheet.write(row_no, 1, value)
        row_no += 1

    # 岗位人数分布情况：
    new_sheet.write_merge(row_no + 1, row_no + 1, 0, 2, '岗位招聘人数分布情况：')
    new_sheet.write(row_no + 2, 0, '招聘人数')
    new_sheet.write(row_no + 2, 1, '岗位数量')
    row_no += 3
    for key, value in ne_dict.items():
        new_sheet.write(row_no, 0, key)
        new_sheet.write(row_no, 1, value)
        row_no += 1

    # 写入社招、应届毕业生招聘人数及比例数据
    new_sheet.write_merge(row_no + 1, row_no + 1, 0, 3, '招聘对象分布及比例：')
    new_sheet.write(row_no + 2, 0, '招聘对象')
    new_sheet.write(row_no + 2, 1, '招聘数量')
    new_sheet.write(row_no + 2, 2, '百分比（%）')
    row_no += 3
    for key, value in employ_type.items():
        new_sheet.write(row_no, 0, key)
        new_sheet.write(row_no, 1, value[0])
        new_sheet.write(row_no, 2, value[1])
        row_no += 1

    # 计算机相关专业、应届毕业生招聘情况数据
    info2 = {'招聘岗位数': [s1_post, s1_post_ratio],
             '招聘人数': [s1_employs, s1_employs_ratio]}

    new_sheet.write_merge(row_no + 1, row_no + 1, 0, 3, '计算机相关专业应届毕业生招聘信息分析')
    new_sheet.write(row_no + 2, 0, '项目')
    new_sheet.write(row_no + 2, 1, '数量')
    new_sheet.write(row_no + 2, 2, '百分比（%）')
    row_no += 3
    for key, value in info2.items():
        new_sheet.write(row_no, 0, key)
        new_sheet.write(row_no, 1, value[0])
        new_sheet.write(row_no, 2, value[1])
        row_no += 1

    # 学历分布情况：
    new_sheet.write_merge(row_no + 1, row_no + 1, 0, 3, '学历分布信息：')
    new_sheet.write(row_no + 2, 0, '最低学历')
    new_sheet.write(row_no + 2, 1, '岗位数')
    new_sheet.write(row_no + 2, 2, '招聘人数')
    new_sheet.write(row_no + 2, 3, '岗位数百分比')
    new_sheet.write(row_no + 2, 4, '人数百分比')
    row_no += 3
    for key, value in s1_academic.items():
        new_sheet.write(row_no, 0, key)
        new_sheet.write(row_no, 1, value[0])
        new_sheet.write(row_no, 2, value[1])
        new_sheet.write(row_no, 3, value[2])
        new_sheet.write(row_no, 4, value[3])
        row_no += 1

    # 综合分析数据
    new_sheet2 = new_work.add_sheet('部门招聘信息分析')
    new_sheet2.write_merge(0, 0, 0, 5, '招聘岗位表部门招聘信息分析结果')
    row_label = ['主管部门', '招聘人数', '占比（%）', '招聘社会人员数量',
                 '招聘应届毕业生数量', '不限人员数量',
                 '社会人员比例', '应届毕业生比例', '不限比例']

    for col, label in enumerate(row_label):
        new_sheet2.write(1, col, label)

    row_no2 = 2

    for key, value in employ_manages.items():
        new_sheet2.write(row_no2, 0, key)
        for col, v in enumerate(value):
            new_sheet2.write(row_no2, col + 1, v)
        row_no2 += 1

    # 保存文件
    new_work.save('./datas/analysis_info.xls')
