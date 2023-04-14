# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/13
# Desc  : 获取KFC餐厅地址数据
import json

import requests


def kfc_info(provinceName):
    """
    获取KFC餐厅地址数据
    """
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'
    }
    param = {
        'cname': '',
        'pid': '',
        'keyword': provinceName,
        'pageIndex': 1,
        'pageSize': 10,
    }
    requests_get = requests.get(url=url, headers=header, params=param)
    get_text = requests_get.text
    # 将文本数据转换为json类型
    return json.loads(get_text)


def data_param(text_list):
    """
    解析数据
    """
    for row in text_list['Table1']:
        print("省市: %s/%s" % (row['provinceName'], row['cityName']))
        print("餐厅名称: " + row['storeName'])
        print("餐厅地址: " + row['addressDetail'])
        print("#########################")


def test_data():
    data = {"Table": [{"rowcount": 50}], "Table1": [{"rownum": 1, "storeName": "银盆路", "addressDetail": "湖南银双路奥克斯广场一楼餐厅", "pro": "Wi-Fi,点唱机,礼品卡", "provinceName": "湖南省", "cityName": "长沙市"},
                                                    {"rownum": 2, "storeName": "桐梓坡", "addressDetail": "湖南桐梓坡路星电光城一层", "pro": "Wi-Fi,点唱机,店内参观,礼品卡", "provinceName": "湖南省", "cityName": "长沙市"},
                                                    {"rownum": 3, "storeName": "国庆", "addressDetail": "湖南人民东路1号", "pro": "Wi-Fi,点唱机,礼品卡", "provinceName": "湖南省", "cityName": "郴州市"},
                                                    {"rownum": 4, "storeName": "麓山", "addressDetail": "湖南清水路59号麓山中南商业广场麓山", "pro": "Wi-Fi,点唱机,店内参观,礼品卡", "provinceName": "湖南省",
                                                     "cityName": "长沙市"},
                                                    {"rownum": 5, "storeName": "株洲月塘", "addressDetail": "湖南新华路华润万家购物广场一楼肯德基餐厅", "pro": "Wi-Fi,点唱机,店内参观,礼品卡", "provinceName": "湖南省",
                                                     "cityName": "株洲市"},
                                                    {"rownum": 6, "storeName": "DT株洲尚格", "addressDetail": "湖南株洲大道尚格名城尚格DT肯德基餐厅", "pro": "点唱机,礼品卡", "provinceName": "湖南省", "cityName": "株洲市"},
                                                    {"rownum": 7, "storeName": "宁波学府", "addressDetail": "钱湖南路666号B座101室", "pro": "Wi-Fi,点唱机,店内参观,礼品卡", "provinceName": "浙江省",
                                                     "cityName": "宁波市"},
                                                    {"rownum": 8, "storeName": "北湖", "addressDetail": "北湖南路南棉街南城百货一层肯德基", "pro": "24小时,Wi-Fi,点唱机,店内参观,礼品卡", "provinceName": "广西",
                                                     "cityName": "南宁市"},
                                                    {"rownum": 9, "storeName": "南京肯德基有限公司盱眙大润发", "addressDetail": "盱眙县都梁大道与东湖南路交汇处", "pro": "Wi-Fi,点唱机,店内参观,礼品卡", "provinceName": "江苏省",
                                                     "cityName": "淮安市"},
                                                    {"rownum": 10, "storeName": "南昌高铁餐厅", "addressDetail": "红谷滩新区九龙湖南昌西站进站内场候车厅肯德基", "pro": "Wi-Fi,点唱机,礼品卡", "provinceName": "江西省",
                                                     "cityName": "南昌市"}]}
    print(data['Table1'])


if __name__ == '__main__':
    provinceName = '北京'
    info_json = kfc_info(provinceName)
    data_param(info_json)
