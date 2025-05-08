# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-05-08
# Desc  : 指定图片生成词云图
import os
from os import path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use('Agg')  # 在导入pyplot之前设置
from matplotlib import pyplot as plt
from wordcloud import ImageColorGenerator, WordCloud


def official_simple():
    import os

    from os import path
    from wordcloud import WordCloud

    # get datas directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, 'datas/constitution.txt')).read()

    # Generate a word cloud image
    wordcloud = WordCloud(background_color='white',  # 背景色为白色
                          height=400,  # 高度设置为400
                          width=800,  # 宽度设置为800
                          scale=20,  # 长宽拉伸程度设置为20
                          prefer_horizontal=0.9999).generate(text)
    plt.figure(figsize=[8, 4])
    plt.imshow(wordcloud)
    plt.axis('off')
    '''保存到本地'''
    plt.savefig('./datas/词云图_official_simple.png', dpi=600, bbox_inches='tight')
    print("保存成功: ./datas/词云图_official_simple.png")
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()


def official_masked():
    """
    Masked wordcloud
    ================

    Using a mask you can generate wordclouds in arbitrary shapes.
    """

    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt

    from wordcloud import WordCloud, STOPWORDS

    # get datas directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, 'datas/alice.txt')).read()

    # read the mask image
    # taken from
    # http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
    alice_mask = np.array(Image.open(path.join(d, "datas/美团外卖logo蒙版.png")))

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
                   stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file(path.join(d, "datas/词云图_official_masked.png"))
    print("保存成功:　./datas/词云图_official_masked.png")

    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def american_word_cloud_chart():
    """美国词云图"""
    # get datas directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, 'datas/alice.txt')).read()

    usa_mask = np.array(Image.open('datas/美国地图蒙版_星条旗色.png'))
    image_colors = ImageColorGenerator(usa_mask)

    '''从文本中生成词云图'''
    wordcloud = WordCloud(background_color='white',  # 背景色为白色
                          height=400,  # 高度设置为400
                          width=800,  # 宽度设置为800
                          scale=20,  # 长宽拉伸程度程度设置为20
                          prefer_horizontal=0.2,  # 调整水平显示倾向程度为0.2
                          mask=usa_mask,  # 添加蒙版
                          max_words=1000,  # 设置最大显示字数为1000
                          relative_scaling=0.3,  # 设置字体大小与词频的关联程度为0.3
                          max_font_size=80  # 缩小最大字体为80
                          ).generate(text)

    plt.figure(figsize=[8, 4])
    plt.imshow(wordcloud.recolor(color_func=image_colors), alpha=1)
    plt.axis('off')
    plt.savefig('./datas/词云图_美国.png', dpi=600, bbox_inches='tight')
    print('保存成功: 词云图_美国')
    plt.show()


def meituan_word_cloud_chart():
    """美团词云图"""

    meituan_mask = np.array(Image.open('datas/美团外卖logo蒙版.png'))
    image_colors = ImageColorGenerator(meituan_mask)
    comments = open(r"datas/culture_words.txt", encoding="utf-8").read()

    '''从文本中生成词云图'''
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/simkai.ttf",  # 定义SimHei字体文件
                          background_color='white',  # 背景色为白色
                          height=400,  # 高度设置为400
                          width=800,  # 宽度设置为800
                          scale=20,  # 长宽拉伸程度程度设置为20
                          prefer_horizontal=0.2,  # 调整水平显示倾向程度为0.2
                          mask=meituan_mask,  # 添加蒙版
                          max_words=1000,  # 设置最大显示字数为1000
                          relative_scaling=0.3,  # 设置字体大小与词频的关联程度为0.3
                          max_font_size=80  # 缩小最大字体为80
                          ).generate(comments)

    plt.figure(figsize=[8, 4])
    plt.imshow(wordcloud.recolor(color_func=image_colors), alpha=1)
    plt.axis('off')
    plt.savefig('./datas/词云图_美团.png', dpi=600, bbox_inches='tight')
    print('保存成功: 词云图_美团')
    plt.show()


if __name__ == '__main__':
    american_word_cloud_chart()
    meituan_word_cloud_chart()
    official_simple()
    official_masked()
