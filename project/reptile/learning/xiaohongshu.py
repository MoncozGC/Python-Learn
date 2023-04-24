# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/19
# Desc  : 使用集成的库获取小红书的数据
# 开源项目:　https://github.com/ReaJason/xhs
from xhs import XhsClient

# 网页访问小红书首页: https://www.xiaohongshu.com/explore, 登录获取cookie
# 开启F12, 查看 https://edith.xiaohongshu.com/api/sns/web/v1/homefeed 接口的cookie
cookie = "----"
xhs_client = XhsClient(cookie)

# 获取笔记内容
text = xhs_client.get_note_by_id("643b522c00000000130331c5")
print(text)

# # 获取用户信息
# xhs_client.get_user_info("5ff0e6410000000001008400")
#
# # 获取用户全部的笔记
# xhs_client.get_user_all_notes("63273a77000000002303cc9b")
#
# # 获取笔记全部的评论
# print(xhs_client.get_note_all_comments("63db8819000000001a01ead1"))

# # 搜索笔记
# xhs_client.get_note_by_keyword("小红书")
#
# # 下载笔记图片或视频到指定路径下
# # 实际会下载到以笔记标题为文件夹名下
# # 例如：C:\Users\User\Desktop\笔记标题\图片.png
# xhs_client.save_files_from_note_id("63db8819000000001a01ead1",
#                                    r"C:\Users\User\Desktop")
