# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/24 15:13
# Desc  :
# encoding: utf-8
"""
@author: seakingx
@contact: hndm@qq.com
@version: 1.0
@file: doex.py
@time: 2020/3/27 0019 09:39
说明 建立百分比的柱状图
"""
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts.charts import *
from pyecharts import options as opts


def create_bar(bar_dict):
    # 建立百分比的柱状图
    bar_item = bar_dict['item']
    bar_head = bar_dict['head']
    bar_data = bar_dict['data']
    print(bar_head)
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(bar_item)
            .set_global_opts(title_opts=opts.TitleOpts(title="销售情况", subtitle="占比情况"))
    )
    for i in range(len(bar_head)):
        bar.add_yaxis(bar_head[i], bar_data[i], label_opts=opts.LabelOpts(formatter="{c} %"))
    bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} %"), interval=10))
    return bar


def get_data_dict():
    # 这里获取要显示的数据 ， 可以改成连接数据库
    data_a = [round(n * 100, 2) for n in [0.2155, 0.423, 0.351, 0.4422, 0.651, 0.722]]
    data_b = [round(n * 100, 2) for n in [0.1233, 0.231, 0.4522, 0.5612, 0.6667, 0.745]]
    pdt_list = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    data_dict = {'data': [data_a, data_b], 'head': ['商家甲', '商家乙'], 'item': pdt_list}
    return data_dict


# 导入要使用的模块
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType


# 将每个图 封装到 函数

# 1.条形图
def bar_datazoom_slider() -> Bar:
    c = (

        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
        .add_xaxis(Faker.days_attrs)
        .add_yaxis("商家A", Faker.days_values)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-水平）"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c


# 2.带标记点的折线图
def line_markpoint() -> Line:
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))

            .add_xaxis(Faker.choose())
            .add_yaxis(
            "商家A",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
            .add_yaxis(
            "商家B",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-MarkPoint"))
    )
    return c


# 3.玫瑰型饼图
def pie_rosetype() -> Pie:
    v = Faker.choose()
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))

            .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )

            .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图示例"))
    )
    return c


# 表格
def table_base() -> Table:
    table = Table()

    headers = ["City name", "Area", "Population", "Annual Rainfall"]
    rows = [
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Adelaide", 1295, 1158259, 600.5],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="Table")
    )
    return table


def page_simple_layout():
    #    page = Page()   默认布局
    page = Page(layout=Page.SimplePageLayout)  # 简单布局
    # 将上面定义好的图添加到 page
    page.add(
        bar_datazoom_slider(),
        line_markpoint(),
        pie_rosetype(),
        table_base(),
    )
    page.render("page_simple_layout.html")


if __name__ == "__main__":
    page_simple_layout()

# if __name__ == "__main__":
# data = get_data_dict()
# bar = create_bar(data)
# bar.render()

# 虚假数据
# x_data = ['Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Meizu']
# y_data_1 = [123, 153, 89, 107, 98, 23]
# y_data_2 = [32, 213, 60, 167, 142, 45]
# bar_1 = Bar()
# bar_1.add_xaxis(
#     x_data
# )
# bar_1.add_yaxis(
#     '系列1',
#     y_data_1,
#     color='green'
# )
#
# bar_2 = Bar()
# bar_2.add_xaxis(
#     x_data
# )
# bar_2.add_yaxis(
#     '系列2',
#     y_data_2,
#     color='rgb(199, 0, 0, 0.2)'
# )
#
# grid = Grid()
# grid.add(bar_1, grid_index=0, grid_opts=opts.GridOpts(pos_right="5%", pos_left="55%"))
# grid.add(bar_2, grid_index=1, grid_opts=opts.GridOpts(pos_right="55%", pos_left="5%"))
#
# grid.render_notebook()
#
# bar_1.render('ceshi.html')
