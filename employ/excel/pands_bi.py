# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/10/21 10:56
# Desc  : pands可视化
# https://www.jianshu.com/p/1f16b382e998 pandas可视化
# Excel成绩指标
#   http://www.360doc.com/content/20/0318/14/54593815_900113534.shtml - Excel制作学生成绩正态分布图
#   https://blog.csdn.net/ydr888/article/details/105050089/
#   https://blog.csdn.net/qq_55977554/article/details/122667432 - 基于pandas的成绩分析可视化
#   https://www.cnblogs.com/linzhen1/p/14922144.html  - Python学生成绩数据可视化与排名预测
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('./datas/2022.xls', sheet_name='Sheet2', header=0)
    print(df)

    df_plot = df.plot(x='班级', y='第一次', kind='barh', stacked=True)
    plt.show()

    # 柱状图bar
    x = range(8)
    y = [100, 200, 400, 350, 450, 350, 250, 300]
    plt.figure(figsize=(20, 8), dpi=80)
    plt.bar(x, y, width=0.4, color=['r', 'k', 'y', 'g', 'b', 'c', 'm', 'k'], label='Bar_x_y')  # 这里是bar()函数
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    # 修改x刻度名字
    plt.xticks(x, ['class1', 'class2', 'class3', 'calss4', 'class5', 'class6', 'class7', 'calss8'])
    # 设置xy标签
    plt.xlabel('Classes')
    plt.ylabel('Numbers')
    plt.title('the Numbers of Classes')

    # plt.savefig('./test1.7.png')
    plt.show()
