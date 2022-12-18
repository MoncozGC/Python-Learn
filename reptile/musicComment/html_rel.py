# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/7/15 16:24
# Desc  :
# 导入requests第三方库，导入报错则需要安装该库
import requests

# 要爬取的url，注意：在开发者工具中这个时候是要找数据对应的url，而不是第一个url
url = "https://api.bilibili.com/x/space/arc/search"
# 模仿浏览器的headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
# 需要的参数
params = {
    "mid": 387694560,
    "pn": 1,
    "ps": 25,
    "index": 1,
    "jsonp": "jsonp"
}
# 调用get方法，传入参数，返回结果集
resp = requests.get(url, headers=headers, params=params)
# 将结果以转化成js格式
js = resp.json()
# 获取js中我们需要的数据集
infos = js['data']['list']['vlist']
# 以下代码为遍历数据
bli = []
for info in infos:
    li = []
    author = info['author']
    bvid = info['bvid']
    pic = info['pic']
    title = info['title']

    li.append(author)
    li.append(bvid)
    li.append(pic)
    li.append(title)
    bli.append(li)
# 输出完整数据
for ll in bli:
    print(ll)
