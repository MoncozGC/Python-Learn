# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/10 17:48
# Desc  : 根据权重值获取1的占位最多且数值最大的数据
# eg: '11100', '10101', '10001'. 1和2两组数据中, 1和2是占位最多的两条数据 且 还要获取到他们数值最大的数据, 也就是返回第一条

import pandas as pd

if __name__ == '__main__':
    data = {'cmnzn': ['A', 'A', 'B', 'B', 'C', 'C'],
            'matching_weight': ['11100', '10101', '10001', '10001', '11010', '11100']}
    data_df = pd.DataFrame(data)

    # 计算每一行中1的个数
    # 使用lambda对max_weight的每一行数据进行判断, 如果等于1, 就进行1的累加
    data_df['max_weight'] = data_df['matching_weight'].apply(lambda x: sum(1 for char in x if char == '1'))
    # 选取列进行降序
    df_sorted = data_df.sort_values(by=['max_weight', 'matching_weight'], ascending=[False, False])
    # 获取
    df_ = df_sorted.groupby('cmnzn').first().reset_index()
    print(df_)
