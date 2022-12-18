# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/6/8 13:52
# Desc  : 进度条

# from time import sleep
#
# print()
# max = 13247
# for i in range(max + 1):
#     print("\r完成进度{0}%".format(i * 100 / max), end="", flush=True)
#     sleep(0.1)

from time import sleep
from tqdm import tqdm

for i in tqdm(range(13247)):
    sleep(0.001)