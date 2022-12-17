# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/2/16 22:19
# Desc  : 生成一段时间区间内的日期

import datetime


def create_assist_date(date_start=None, date_end=None):
    # 创建日期辅助表

    if date_start is None:
        date_start = '2016-01-01'
    if date_end is None:
        date_end = datetime.datetime.now().strftime('%Y-%m-%d')

    # 转为日期格式
    date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    date_list = []
    date_list.append(date_start.strftime('%Y-%m-%d'))
    while date_start < date_end:
        # 日期叠加一天
        date_start += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(date_start.strftime('%Y-%m-%d'))
    return date_list


if __name__ == '__main__':
    d_list = create_assist_date(date_start='2021-12-27', date_end='2021-12-30')
    print(d_list)
