# Author: MoncozGC
# Date  : 2021/12/8 16:27
# Desc  : jieba分词官方用例
# encoding=utf-8
import jieba

# jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
# value = ["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
# for values in value:
#     seg_list = jieba.cut(values, use_paddle=True) # 使用paddle模式
#     print("Paddle Mode: " + '/'.join(list(seg_list)))
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))

testStr = '维生素E软胶囊(维生素E软胶囊'
# 搜索引擎模式
search = jieba.cut_for_search(testStr)
print(", ".join(search))
# 精准模式
searchCut = jieba.cut(testStr)
print(", ".join(searchCut))