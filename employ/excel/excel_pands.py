# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/20 15:00
# Desc  : pands操作excel
# 数据分析思路: 每个班级的平均分、最高分、最低分、中位数; 第一次和第二次的数据对比(环比)
# 指标: 优秀率: > 108, > 108的人数 / 班级总人数. 【及格率、不及格率】
# 将方法集成, 多个数据条数对比可以作为一个方法

import copy
import csv

import xlrd
from matplotlib import pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
import pandas as pd
from utils.comm_util import print_ts

# 读取数据文件路径
input_file = './datas/2022.xls'
# 生成结果文件路径
out_file = './result'
# 指定Sheet名称
sheet_name = 'Sheet1'
# 指定从第几行开始读, 从0开始
rows = 0
# 指定成绩分数列, [第一个参数为分组名称, 其余为往期成绩, ...]
specify_colum = ['班级', '第一次', '第二次']


def get_extreme_score(_stu_max, _stu_min):
    """
    获取最高分\最低分. 成绩及姓名
    :param _stu_max: 最高分
    :param _stu_min: 最低分
    :return:
    """
    open_workbook = xlrd.open_workbook(input_file)
    # sheet页, 从0开始
    sheet = open_workbook.sheet_by_index(0)
    # 按行读取表格数据, 从第三行开始读取
    all_data = sheet._cell_values[2:]

    # 获取学生姓名一栏
    students = ([ds[2] for ds in all_data])
    students_manages = {key: [0, 0, 0, 0] for key in students}
    # 将学生对应的分数存储起来
    for ds in all_data:
        if ds[2] in students_manages.keys():
            students_manages[ds[2]][0] += int(ds[10])

    # dropna删除掉空的数据
    # https://blog.csdn.net/beilizhang/article/details/111399597
    max_score = max([int(ds) for ds in _stu_max['第一次'].dropna(how='all')])
    min_score = min([int(ds) for ds in _stu_min['第一次'].dropna(how='all')])
    print_ts("成绩[最高分\最低分]: ", max_score, min_score)

    # 根据成绩获取到对应的姓名
    max_stu = [key for key in students_manages.keys()
               if students_manages[key][0] == max_score]
    min_stu = [key for key in students_manages.keys()
               if students_manages[key][0] == min_score]

    print_ts("姓名[最高分\最低分]: ", max_stu, min_stu)


def get_base_info(_colum_name, _specify_colum):
    """
    获取成绩的基本信息
    :param _colum_name: 基本数据
    :param _specify_colum: 成绩列名
    :return:
    """
    # 获取班级平均分: mean
    stu_avg = _colum_name.groupby(_specify_colum[0]).mean().reset_index().sort_values(_specify_colum[1],
                                                                                      ascending=False,
                                                                                      ignore_index=True)
    # 排序方式: https://www.jb51.net/article/262643.htm
    # 根据名称倒叙排序, 生成轴从0开始
    print_ts("平均分, 从高到低排序: \n", stu_avg)

    class_num = len(stu_avg[_specify_colum[1]].dropna(how='all'))
    print_ts("有效成绩的班级: ", class_num)

    stu_median = _colum_name.groupby(by=[_specify_colum[0]]).median().reset_index().sort_values(_specify_colum[1],
                                                                                                ascending=False,
                                                                                                ignore_index=True)
    print_ts("中位数， 从高到低排序: \n", stu_median.head(5))

    stu_max = _colum_name.groupby(by=[_specify_colum[0]]).max().reset_index().sort_values(_specify_colum[1],
                                                                                          ascending=False,
                                                                                          ignore_index=True)
    print_ts("最高分, 从高到低排序: \n", stu_max.head(5))

    stu_min = _colum_name.groupby(_specify_colum[0]).min().reset_index().sort_values(_specify_colum[1], ascending=True,
                                                                                     ignore_index=True)
    print_ts("最低分, 从低到高排序: \n", stu_min.head(5))

    # TODO 1.2 获取最高分\最低分姓名
    get_extreme_score(stu_max, stu_min)

    # TODO 不及格人数


def get_senior_info(_colum_name, _specify_colum):
    """
    获取环比成绩信息
    :param _colum_name: 分组主键字段
    :param _specify_colum_1: 上期成绩
    :param _specify_colum_2: 本期成绩
    :return:
    """
    colum_senior = df[[_colum_name, '学生姓名', _specify_colum[1], _specify_colum[2]]]

    # 生成df之后再加上一列, 剔除警告
    colum_senior_info = pd.DataFrame(colum_senior)
    # pands新增列
    colum_senior_info.loc[:, 'ring_ratio'] = 0

    print_ts("colum", colum_senior_info)

    # 计算环比值
    for i in range(0, len(colum_senior_info)):
        # loc[某行, 指定列]
        colum_senior_info.loc[i, 'ring_ratio'] = format(
            (colum_senior_info['第二次'][i] - colum_senior_info['第一次'][i]) / colum_senior_info['第一次'][i], '.2')

    print_ts("两次成绩的环比值 \n", colum_senior_info.head(5))

    # 根据环比值获取环比画布图
    get_ratio(colum_senior_info)


def get_ratio(_senior_result):
    """
    根据环比生成图
    :return:
    """
    student_id = [str(i) for i in _senior_result['学生姓名']]
    ring_ratio = [str(i) for i in _senior_result['ring_ratio']]
    bar = (
        # https://www.iotword.com/2247.html - pyecharts绘制各种数据可视化图表案例
        Bar(init_opts=opts.InitOpts(width="1550px", height="2250px"))
            .add_xaxis(student_id)  # x轴数据
            .add_yaxis('环比', ring_ratio)  # y轴数据
            # 反转画布
            .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title="环比生成图"),
                             xaxis_opts=opts.AxisOpts(name_rotate=80, axislabel_opts={"rotate": 450}))
            .set_series_opts(
            label_opts=opts.LabelOpts(position="right"),
        )
    )
    bar.render(out_file + '/环比生成图.html')


def canvas_get_number(_specify_colum, _compare_value, _judge):
    """
    获取人数
    :param _judge:
    :param _compare_value:
    :param _specify_colum:
    :return:
    """
    stu_eliminate = colum_base_info.groupby(by=[_specify_colum[0]])

    # 转换为list
    apply = stu_eliminate['第一次'].apply(list)

    # 获取对应班级及成绩
    stu_storage = []
    t = 0
    for j in apply:
        # 获取索引值
        # print_ts("班级: ", apply.index[t])
        out = 0
        # 根据成绩list的长度, 获取对应的学生成绩
        for i in range(len(j)):
            if _judge == 'out':
                # 不及格人数
                if j[i] < _compare_value:
                    # print_ts("学生成绩: ", j[i])
                    out += 1
            elif _judge == 'goods':
                # 优秀人数
                if j[i] > _compare_value:
                    # print_ts("学生成绩: ", j[i])
                    out += 1
        stre = str(apply.index[t]) + "_" + str(out)
        t += 1
        # print_ts("不及格人数: ", out)
        if stre not in stu_storage:
            # 将数据放入list中
            stu_storage.append(stre)
    # print_ts("不及格人数生成画布", stu_storage)
    # 根据拼接下划线获取
    # print_ts(stu_storage[0].split("_")[1])

    # 根据不及格人数生成图
    student_id = [str(i).split("_")[0] for i in stu_storage]
    ring_ratio = [str(i).split("_")[1] for i in stu_storage]

    # print_ts("不及格人数输出对应班级: ", student_id)
    # print_ts("输出对应成绩: ", ring_ratio)

    # 不及格人数生成图
    bar = (
        # https://www.iotword.com/2247.html - pyecharts绘制各种数据可视化图表案例
        Bar(init_opts=opts.InitOpts(width="1550px", height="1250px"))
            .add_xaxis(student_id)  # x轴数据
            .add_yaxis('人数', ring_ratio)  # y轴数据
            # 反转画布
            .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title="不及格人数生成图"),
                             xaxis_opts=opts.AxisOpts(name_rotate=80, axislabel_opts={"rotate": 450}))
        #     .set_series_opts(
        #     label_opts=opts.LabelOpts(position="right"),
        # )
    )
    # bar.render(out_file + '/不及格人数生成图.html')
    # return bar
    return student_id, ring_ratio


def canvas_get_rate(_specify_colum, _compare_value, _judge):
    """
    获取比率
    :param _judge:
    :param _compare_value:
    :param _specify_colum:
    :return:
    """
    stu_eliminate = colum_base_info.groupby(by=[_specify_colum[0]])

    # 转换为list
    apply = stu_eliminate['第一次'].apply(list)

    # 获取对应班级及成绩
    stu_storage_rate = []
    stu_storage_nuber = []
    t = 0
    for j in apply:
        # 获取索引值
        # print_ts("班级: ", apply.index[t])
        out = 0
        # 根据成绩list的长度, 获取对应的学生成绩
        for i in range(len(j)):
            if _judge == 'out':
                # 不及格人数
                if j[i] < _compare_value:
                    # print_ts("学生成绩: ", j[i])
                    out += 1
            elif _judge == 'goods':
                # 优秀人数
                if j[i] > _compare_value:
                    out += 1
            elif _judge == 'pass':
                # 及格人数
                if j[i] > _compare_value:
                    out += 1
        # 比率计算: 将分数转换为整数
        c = round(out / len(j) * 100)
        str_rate = str(apply.index[t]) + "_" + str(c)
        str_number = str(apply.index[t]) + "_" + str(out)
        t += 1
        # print_ts("不及格人数: ", out)
        if str_rate not in stu_storage_rate:
            # 将数据放入list中
            stu_storage_rate.append(str_rate)
        if str_number not in stu_storage_nuber:
            # 将数据放入list中
            stu_storage_nuber.append(str_number)

    print_ts("比率-画布", stu_storage_rate)
    print_ts("数量-画布", stu_storage_nuber)

    # 根据不及格人数生成图
    student_id = [str(i).split("_")[0] for i in stu_storage_rate]
    # 数量
    data_number = [str(int(str(i).split("_")[1])) for i in stu_storage_nuber]
    # 比率
    data_rate = [str(int(str(i).split("_")[1]) / 100) for i in stu_storage_rate]

    # 不及格人数生成图
    bar = (
        # https://www.iotword.com/2247.html - pyecharts绘制各种数据可视化图表案例
        Bar(init_opts=opts.InitOpts(width="1550px", height="1250px"))
            .add_xaxis(student_id)  # x轴数据
            .add_yaxis('人数', data_rate)  # y轴数据
            # 反转画布
            # .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title="不及格人数生成图"),
                             # 添加双线条
                             tooltip_opts=opts.TooltipOpts(
                                 is_show=True, trigger="axis", axis_pointer_type="cross"
                             ),
                             xaxis_opts=opts.AxisOpts(
                                 type_="category",
                                 axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                             ),
                             )
            .set_series_opts(
            label_opts=opts.LabelOpts(position="right"),
        )
    )
    bar.render(out_file + '/不及格人数生成图.html')
    # return bar
    return student_id, data_number, data_rate


def canvas_get_avg(_specify_colum):
    """
    获取班级平均分画布
    :return:
    """
    stu_avg = colum_base_info.groupby(by=[_specify_colum[0]]).mean()
    avg_list = stu_avg['第一次'].tolist()

    stu_storage = []
    a = 0
    # 班级循环, 从2201->2238. 处理班级数据有可能缺失的情况
    for x in range(2201, 2238):
        for i in stu_avg:
            if stu_avg.values[a] > 0:
                # 拼接字符串
                stre = str(x) + "_" + str(int(stu_avg.values[a] * 100))
            else:
                stre = str(stu_avg.index[a]) + "_" + str(0)
            a += 1
            if stre not in stu_storage:
                stu_storage.append(stre)

    print_ts("平均分画布: ", stu_storage)

    # 根据平均值生成图
    student_id = [str(i).split("_")[0] for i in stu_storage]
    # 将数据 / 100, 保留两位小数
    ring_ratio = [str(int(str(i).split("_")[1]) / 100) for i in stu_storage]
    print_ts("平均分输出对应班级: ", student_id)
    print_ts("输出对应成绩: ", ring_ratio)

    bar = (
        # https://www.iotword.com/2247.html - pyecharts绘制各种数据可视化图表案例
        Bar(init_opts=opts.InitOpts(width="1550px", height="1050px"))
            .add_xaxis(student_id)  # x轴数据
            .add_yaxis('平均分分数', ring_ratio, color='#1EA5C0')  # y轴数据
            # 反转画布
            # .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title="班级平均分"),
                             xaxis_opts=opts.AxisOpts(name_rotate=80, axislabel_opts={"rotate": 450}))
            .set_series_opts(
            label_opts=opts.LabelOpts(position="right"),
        )
    )
    # bar.render(out_file + '/班级平均分.html')

    return bar
    # return student_id, ring_ratio

def canvas_data(_specify_colum):
    """
    # 及格\优秀\不及格 - 指标数据
    :return:
    """
    # 及格\优秀\不及格 - 指标数据
    pass_ids, pass_number, pass_rate = canvas_get_rate(_specify_colum, 72, 'pass')
    goods_ids, goods_number, goods_rate = canvas_get_rate(_specify_colum, 108, 'goods')
    out_ids, out_number, out_rate = canvas_get_rate(_specify_colum, 72, 'out')

    barc = (
        Bar(init_opts=opts.InitOpts(height="2150px"))
            .add_xaxis(pass_ids)
            .add_yaxis("及格率", pass_rate)
            .add_yaxis("优秀率", goods_rate)
            .add_yaxis("不及格率", out_rate)
            .reversal_axis()
            .set_global_opts(
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="数据对比", subtitle="及格率、优秀率、不及格率"), )
            .set_series_opts(label_opts=opts.LabelOpts(position="right"), )
    )

    c = (
        Bar(init_opts=opts.InitOpts(height="2150px"))
            .add_xaxis(pass_ids)
            .add_yaxis("及格人数", pass_number)
            .add_yaxis("优秀人数", goods_number)
            .add_yaxis("不及格人数", out_number)
            .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="数据对比", subtitle="及格人数、优秀人数、不及格人数"),
            # 数据缩放滑块
            # datazoom_opts=opts.DataZoomOpts(),
        )
            .set_series_opts(label_opts=opts.LabelOpts(position="right"), )
    )

    page_simple_layout(_specify_colum, barc, c)


def page_simple_layout(_specify_colum, _layout_1, _layout_2):
    """
    将画布全部输出到一个文件中
    :param _specify_colum:
    :return:
    """
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        _layout_1,
        _layout_2,
    )
    page.render(out_file + "/学生成绩数据分析.html")


if __name__ == '__main__':
    # df = pd.read_excel(inputfile, sheet_name='Sheet1', header=1)
    df = pd.read_excel(input_file, sheet_name=sheet_name, header=rows)

    print_ts("读取文件: ", input_file)
    print_ts("读页信息: ", sheet_name)
    print_ts("轮询字段: ", specify_colum)

    colum_base_info = df[[specify_colum[0], specify_colum[1]]]
    # print(colum_name)

    # TODO 1.1 获取成绩的基本信息
    get_base_info(colum_base_info, specify_colum)

    # TODO 1.3 获取环比成绩信息
    get_senior_info(specify_colum[0], specify_colum)

    # 根据不及格率生成画布
    # get_canvas(specify_colum)
    # 根据平均分生成画布
    # avg_canvas(specify_colum)

    # 整合画布到一个文件中
    # page_simple_layout(specify_colum)

    # 及格\优秀\不及格 - 指标数据生成到一个文件中
    canvas_data(specify_colum)
