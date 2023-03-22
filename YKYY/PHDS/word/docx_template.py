# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/1/12 14:52
# Desc  : 通过word模板, 写入参数数据

from docxtpl import DocxTemplate

data = {
    't1': '燕子',
    't2': '杨柳',
    't3': '桃花',
    't4': '针尖',
    't5': '头涔涔',
    't6': '泪潸潸',
    't7': '茫茫然',
    't8': '伶伶俐俐',
}

# 读取模板
template = DocxTemplate("demo.docx")
# 插入数据
template.render(data)
# 生成新的文档
template.save("demov2.docx")
