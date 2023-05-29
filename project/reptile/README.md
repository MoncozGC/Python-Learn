```text
    ├──BReptile.py 爬取B站评论区信息
    ├──wechat_*: 微信聊天记录解析, 生成年度报告中的数据信息【datas/wechat-report.zip vue工程可生成聊天年度报告】
    ├──nCov_2019: 爬取nCov数据信息, 目前该网站已停止更新信息
    ├──weather: 爬取天气信息, 并且入库
    ├──hpv: 预约九价
```

年度报告原项目地址： https://github.com/myth984/wechat-report

## 使用

### 文件写入模式

```python
"""
文件打开模式表示文件用于何种目的，常用的模式如下：

'r': 以只读模式打开文件（默认模式）
'w': 以只写模式打开文件。如果文件不存在，创建文件。如果文件已存在，先清空文件内容，再写入新内容。
'x': 如果文件不存在，创建文件并以只写模式打开。如果文件已存在，则抛出错误。
'a': 以追加模式打开文件。如果文件不存在，创建文件。
'b': 以二进制模式打开文件。
't': 以文本模式打开文件（默认模式）。
'+': 可同时读写文件。
'U': 支持通用换行符。在Python 3.x版本已经废弃。

文件打开模式还可以和操作类型组合，例如：
'rb': 以二进制模式读取文件。
'wb': 以二进制模式写入文件。
'xt': 如果文件不存在，创建文件并以文本模式打开。
'a+': 以读写追加模式打开文件。
在使用文件读写操作时，需根据具体的需求和文件内容来选择适当的打开模式。
"""

with open('file_name', 'w', encoding='utf-8') as fp:
    fp.write("text")
```

### 文本对齐

```python
from lxml import html

# 示例数据
data = '''
<div class="cell item">
<a href="/member/joefuzhou198x">joefuzhou198x</a>
<a href="/t/933384">为什么 chatgpt 以及一系列创新不会出现在中国？为什么创新不能靠举国体制？</a>
<a href="/t/933384#reply252" class="count_livid">252</a>
</div>
<div class="cell item">
<a href="/member/akring">akring</a>
<a href="/t/933373">作为开发者，大家最喜欢的个人主页风格是什么？</a>
<a href="/t/933373#reply140" class="count_livid">140</a>
</div>
'''

tree = html.fromstring(data)

max_user_width = 0
max_title_width = 0

results = []

for item in tree.xpath('//div[@class="cell item"]'):
    user = item.xpath('.//a[contains(@href,"/member/")]/text()')[0]
    title = item.xpath('.//a[contains(@href,"/t/")]/text()')[0]
    url = item.xpath('.//a[contains(@href, "/t/")]/@href')[0]
    url = 'https://www.v2ex.com/' + url
    reply_num = item.xpath('.//a[@class="count_livid"]/text()')[0]

    max_user_width = max(max_user_width, len(user))
    max_title_width = max(max_title_width, len(title))

    results.append({"user": user, "title": title, "url": url, "reply_num": reply_num})

for result in results:
    # :<{width_variable}}表示左对齐, 变量可改变仅是占位符
    print("用户: {user:<{user_width}}\t标题: {title:<{title_width}}\t链接: {url}\t回复数: {reply_num}\t".format(user_width=max_user_width, title_width=max_title_width, **result))

```

### 判断文件是否有内容

```python
import os.path

# true: 无内容, false: 有内容
is_file_empty = os.path.getsize('file_name') == 0
```