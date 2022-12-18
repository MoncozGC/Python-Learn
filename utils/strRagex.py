# Author: MoncozGC
# Date  : 2021/12/16 17:00
# Desc  : 正则匹配去除小括号
# encoding: utf-8
import re

string = "本实用新型公开了全自动套鞋机，在机架（1）内安装鞋套弹性进给装置构成套鞋机，在机架（1）的中间安装滑杆（2）"
# 全角字符
res = re.sub(u"\\（.*?\\）|\\{.*?}|\\［.*?］", '', string)
print(res)
# 半角字符
name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", '', string)
print(name)

# 这9个字符在Windows系统下是不可以出现在文件名中的
chara = '*\/:?"<>|'
# 样例
str1 = '\巴拉<1"!11【】>1*hstrgn/p:?|'

# 只要字符串中的中文，字母，数字
str = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', str1, re.S)
str = "".join(str)
print(str)

# 只去除不想要的，比如只去除不能作为文件名的字符
str2 = re.findall(r'[^\*"/:?\\|<>]', str1, re.S)
str2 = "".join(str2)
print(str2)
