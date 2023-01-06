# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/1/5
# Desc  : 时间工具方法

def time_cn_trans(cn_time):
    """
    将中文时间, 转换为数字格式
    eg: 2023年1月1日 => 2023-01-01
    :param cn_time: 
    :return: 
    """
    chinese_data_dict = {
        '1': '01',
        '2': '02',
        '3': '03',
        '4': '04',
        '5': '05',
        '6': '06',
        '7': '07',
        '8': '08',
        '9': '09',
    }

    year = cn_time.split('年')[0]
    month = cn_time.split('年')[1].split('月')[0]
    day = cn_time.split('年')[1].split('月')[1].split('日')[0]

    i = 0
    for c in range(0, 1):
        month_len = len(cn_time.split('年')[1].split('月')[i])
        day_len = len(cn_time.split('年')[1].split('月')[1].split('日')[i])
        if month_len == 1:
            month = month.replace(month, chinese_data_dict[month])
        if day_len == 1:
            day = day.replace(day, chinese_data_dict[day])

        i = i + 1
    cn_time = year + '-' + month + '-' + day
    return cn_time
