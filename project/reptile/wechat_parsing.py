"""
encoding: utf-8
Author: MoncozGC
Date  : 2022/1/3 23:40
Desc  : 解析微信聊天记录存储到数据库中的数据
"""
import functools

import pymysql
import jieba
import json

# 读取停用词列表
def get_stropword_list(file):
    with open(file, 'r', encoding='utf-8') as f:
        stopWord_list = [word.strip('\n') for word in f.readlines()]
    return stopWord_list


# 分词 然后去除停用词
def clean_stopWord(str, stopword_list):
    result = []
    # 分词后返回一个列表
    # jieba.lcut 返回的是一个迭代器
    word_list = jieba.lcut(str)
    for w in word_list:
        if w not in stopword_list:
            result.append(w)
    return result


stopword_file = r'datas/stopwords.txt'
# 获得停用词列表
stopword_list = get_stropword_list(stopword_file)

conn = pymysql.connect(
    host='192.168.153.161',
    user='ambari',
    password='ambari',
    db='test',
    charset='utf8mb4',
    port=3306)

cur = conn.cursor()

cur.execute("select * from log")

r = cur.fetchall()
result = {}

# 获得最长的一句话
max_item = None
for item in r:
    content = item[3]
    if (max_item is None or len(content) > len(max_item[3])) and content.find('http') == -1:
        max_item = item
print(max_item)

# # 进行分词
word_arr = []
for item in r:
    content = item[3]
    seg_list = jieba.cut(content)
    word_arr = word_arr + list(seg_list)
    # 使用哈工大停用词
    # word_arr = clean_stopWord(content, stopword_list)
word_count_map = {}
for word in word_arr:
    if word in word_count_map:
        word_count_map[word] = word_count_map[word] + 1
    else:
        word_count_map[word] = 1
word_count_arr = []
for word in word_count_map:
    o = {
        'word': word,
        'count': word_count_map[word]
    }
    word_count_arr.append(o)
    with open('datas/result.txt', "a+", encoding="utf-8") as f2:
        f2.write(f"{word}\t{word_count_map[word]}\n")


def custom_sort(x, y):
    if x['count'] > y['count']:
        return -1
    if x['count'] < y['count']:
        return 1
    return 0


result['word'] = sorted(word_count_arr, key=functools.cmp_to_key(custom_sort))

with open("datas/result.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(result, ensure_ascii=False)
    )

