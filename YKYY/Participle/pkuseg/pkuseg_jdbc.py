# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/1/12 13:27
# Desc  : pkuseg分词器, 连接CK根据字段分词

import pkuseg
from clickhouse_driver import Client

ckClient = Client(host='xxxx', database='bds_dw', user='default', password='default')

seg = pkuseg.pkuseg(model_name='medicine')
sql = "SELECT DISTINCT spuName FROM bds_dw.dws_sku_details_1d_loc WHERE spuName LIKE '%维生素%' "
execute = ckClient.execute(sql)

# 遍历获取sql执行出来的数据, 数据格式是: list包含tuple的数据
for item in execute:
    # 获取list中的tuple数据, 将tuple数据转换为list
    str_reverse = "".join(tuple(item))
    set_cut = seg.cut(str_reverse)
    print(set_cut)

execute.clear()