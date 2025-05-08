# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-05-08
# Desc  :
import re

import jieba
import pandas as pd

'''读入原始数据'''
raw_comments = pd.read_csv('datas/waimai_10k.csv')
raw_comments.head()
'''导入停用词表'''
with open('datas/stopwords.txt', encoding='utf-8') as s:
    stopwords = set([line.replace('\n', '') for line in s])

'''传入apply的预处理函数，完成中文提取、分词以及多余空格剔除'''


def preprocessing(c):
    c = [word for word in jieba.cut(' '.join(re.findall('[\u4e00-\u9fa5]+', c))) if word != ' ' and word not in stopwords]

    return ' '.join(c)


'''将所有语料按空格拼接为一整段文字'''
comments = ' '.join(raw_comments['review'].apply(preprocessing))
print(comments)
