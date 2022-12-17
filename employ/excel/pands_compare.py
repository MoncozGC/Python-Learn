# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/21 9:45
# Desc  : pands计算同比、环比
import random

import pandas as pd

from utils.comm_util import print_ts

if __name__ == '__main__':
    # 生成日期
    date_M = list(pd.date_range('1/1/2019', periods=24, freq='M'))
    money = [random.randint(18000, 20000) for i in range(0, 24)]
    data = pd.DataFrame({'date_M': date_M, 'money': money})

    # 升序排列-按照日期
    data.sort_values(by=['date_M'], inplace=True)

    # 新增列 -'huanbi' 环比的意思
    data.loc[:, 'huanbi_01'] = 0

    # 计算环比列数值
    for i in range(0, len(data)):
        if i == 0:
            data.loc[i, 'huanbi_01'] = 'null'
        else:
            # 环比值 = (当前 - 上一个) / 上一个
            data.loc[i, 'huanbi_01'] = format((data['money'][i] - data['money'][i - 1]) / data['money'][i - 1], '.2%')
            # format(res,'.2%') 小数格式化为百分数

    print(data)
