"""
encoding: utf-8
Author: MoncozGC
Date  : 2022/1/12 10:27
Desc  : pkuseg分词器使用
"""
import pkuseg

seg = pkuseg.pkuseg(model_name='medicine')
test = seg.cut('维生素A')
print(test)
