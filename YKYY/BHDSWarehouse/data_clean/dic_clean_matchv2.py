# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/22 15:19
# Desc  : 数据匹配, 全量及增量更新
if __name__ == '__main__':
    import pandas as pd
    from datetime import datetime, date, timedelta

    # 假设这是你的 clean_dataframe
    clean_dataframe = pd.DataFrame({'cid': [98], 'dis': ['肺脏,脾脏,肾脏'], 'crt': ['2023-03-22']})

    # 假设这是你的 dic_dataframe
    dic_dataframe = pd.DataFrame({'aid': [10, 21, 25], 'poszn': ['肺脏', '脾脏', '肾脏']})


    def process_dataframes(clean_dataframe, dic_dataframe):
        # 将 clean_dataframe 中的 'dis' 列拆分为多行
        clean_dataframe = clean_dataframe.assign(dis=clean_dataframe['dis'].str.split(',')).explode('dis')

        # 将 'dis' 列重命名为 'poszn'，以便与 dic_dataframe 进行合并
        clean_dataframe = clean_dataframe.rename(columns={'dis': 'poszn'})

        # 将 clean_dataframe 与 dic_dataframe 合并，并将 'cid' 列重命名为 'oid'
        result_dataframe = clean_dataframe.merge(dic_dataframe, on='poszn').rename(columns={'cid': 'oid'})

        # 选择 'oid', 'crt' 和 'aid' 列作为最终结果
        result_dataframe = result_dataframe[['oid', 'crt', 'aid']]

        return result_dataframe


    # 首次处理
    result_dataframe = process_dataframes(clean_dataframe, dic_dataframe)
    print(result_dataframe)

    # 增量更新 clean_dataframe
    new_data = pd.DataFrame({'cid': [99], 'dis': ['肺脏,脾脏'], 'crt': ['2023-03-21']})
    new_data2 = pd.DataFrame({'cid': [99], 'dis': ['肺脏,脾脏'], 'crt': ['2023-03-23']})
    clean_dataframe = clean_dataframe.append(new_data, ignore_index=True)
    clean_dataframe = clean_dataframe.append(new_data2, ignore_index=True)

    # 将 crt 列转换为日期时间格式
    clean_dataframe['crt'] = pd.to_datetime(clean_dataframe['crt'])

    # 获取今天的日期
    today = datetime.today().date()

    # 仅筛选 crt 小于今天的数据
    clean_dataframe = clean_dataframe[clean_dataframe['crt'].dt.date < today]

    # 处理更新后的数据
    result_dataframe = process_dataframes(clean_dataframe, dic_dataframe)
    print(result_dataframe)

    print((date.today()).strftime("%Y-%m-%d"))

