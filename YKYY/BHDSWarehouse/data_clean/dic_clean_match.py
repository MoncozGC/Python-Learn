# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/22 15:19
# Desc  : 数据匹配
"""
python, 使用我已经有一个clear_dataframe, 有一列字段dis有一条这样的数据 肺脏,脾脏,肾脏 , 这条数据的cid为98. 还有一个dic_dataframe, 里面有这样的数据: aid字段:10, poszn字段:肺脏; aid字段:21,poszn字段:脾脏; aid字段:25, poszn字段:肾脏. 请使用python的pands将数据处理为一个新的dataframe,结构如下: oid字段为:1, aid字段为:10, oid字段为:1, aid字段为21, oid字段为1,aid字段为25. 一一的将两个dataframe字段中的数据匹配出来
"""
if __name__ == '__main__':
    import pandas as pd

    # 假设这是你的 clear_dataframe
    clear_dataframe = pd.DataFrame({'cid': [98], 'dis': ['肺脏,脾脏,肾脏']})

    # 假设这是你的 dic_dataframe
    dic_dataframe = pd.DataFrame({'aid': [10, 21, 25], 'poszn': ['肺脏', '脾脏', '肾脏']})

    # 将 clear_dataframe 中的 'dis' 列拆分为多行
    clear_dataframe = clear_dataframe.assign(dis=clear_dataframe['dis'].str.split(',')).explode('dis')

    # 将 'dis' 列重命名为 'poszn'，以便与 dic_dataframe 进行合并
    clear_dataframe = clear_dataframe.rename(columns={'dis': 'poszn'})

    # 将 clear_dataframe 与 dic_dataframe 合并，并将 'cid' 列重命名为 'oid'
    result_dataframe = clear_dataframe.merge(dic_dataframe, on='poszn').rename(columns={'cid': 'oid'})

    # 选择 'oid' 和 'aid' 列作为最终结果
    result_dataframe = result_dataframe[['oid', 'aid']]

    print(result_dataframe)
