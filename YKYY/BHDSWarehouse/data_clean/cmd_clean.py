# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/26
# Desc  : 将窄数据转换为宽数据
"""
窄数据列表: data
宽数据:
key   gdszn  gdsen gdson pt
硼砂   硼砂  Borax     湩

pt为补充字段数据, 数据为空
"""
import pandas as pd

if __name__ == '__main__':
    # 创建示例数据
    data = {'cname': ['硼砂', '硼砂', '硼砂', '硼砂', '硼砂', '硼砂', '硼砂', '硼砂'],
            'key': ['中文名称', '拉丁文名', '别名', '性味归经', '药材分类', '功能', '主治', '用法用量'],
            'value': ['硼砂', 'Borax', '湩', '味甘、咸，性凉', '矿物', '清热消痰', '内服，治痰热咳嗽', '内服：入丸、散']}
    data_df = pd.DataFrame(data)

    # 构建字段映射关系
    filed_mapping = {
        '中文名称': 'gdszn',
        '拉丁文名': 'gdsen',
        '别名': 'gdson',
        '注意事项': 'pt'
    }

    # 将key对应的字段数据, 映射为英文数据
    data_df['key'] = data_df['key'].map(filed_mapping)
    data_df = data_df.drop_duplicates(subset=['cname', 'key'])
    # 窄表转换为宽表
    data_df = data_df.pivot(index='cname', columns='key', values='value')
    # 因为数据中出现的字段不是固定的, 但是又需要映射表中的字段. 所以需要将字段添加到df中
    # fillna是将Nan数据装置为空
    data_df = data_df.reindex(columns=list(filed_mapping.values())).fillna(' ')
    print(data_df)
