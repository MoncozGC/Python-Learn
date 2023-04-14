# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/12 19:12
# Desc  : POST请求访问百度翻译

import requests

from utils.comm_util import print_ts


def translation(text):
    print_ts("发起百度翻译POST请求, 翻译文本: %s" % text)
    url = 'https://fanyi.baidu.com/sug'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    # 请求参数
    params = {
        'kw': text
    }
    requests_post = requests.post(url=url, data=params, headers=headers)
    return requests_post.json()


def json_parse(dict_):
    print_ts("解析数据, 翻译结果: ")
    json_data = {'errno': 0, 'data': [{'k': 'dog', 'v': 'n. 狗; 蹩脚货; 丑女人; 卑鄙小人 v. 困扰; 跟踪'}, {'k': 'DOG', 'v': 'abbr. Data Output Gate 数据输出门'}, {'k': 'doge', 'v': 'n. 共和国总督'},
                                      {'k': 'dogm', 'v': 'abbr. dogmatic 教条的; 独断的; dogmatism 教条主义; dogmatist'}, {'k': 'Dogo', 'v': '[地名] [马里、尼日尔、乍得] 多戈; [地名] [韩国] 道高'}]}

    # 获取到这一条数据: n. 狗; 蹩脚货; 丑女人; 卑鄙小人 v. 困扰; 跟踪
    data_ = dict_['data'][0]['v']
    print_ts(data_)


if __name__ == '__main__':
    post_dict = translation("温文尔雅")
    json_parse(post_dict)
