# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/8/23 22:21
# Desc  : 获取虎牙直播源地址
# 获取虎牙直播的真实流媒体地址。
# 虎牙"一起看"频道的直播间可能会卡顿
# 获取虎牙直播的真实流媒体地址。

import base64
import hashlib
import random
import re
import sys
import time
import urllib.parse

import requests


def live(e):
    try:
        i, b = e.split('?')
        r = i.split('/')
        s = re.sub(r'.(flv|m3u8)', '', r[-1])
        c = b.split('&')
        c = [i for i in c if i != '']
        n = {i.split('=')[0]: i.split('=')[1] for i in c}

        fm = urllib.parse.unquote(n['fm']) if ('fm' in n.keys()) else ''
        u = base64.b64decode(fm).decode('utf-8') if ('fm' in n.keys()) else ''
        p = u.split('_')[0]
        f = str(int(time.time() * 1e7))
        l = n['wsTime']

        mt = n['txyp'] if ('txyp' in n.keys()) else 'a'
        t = str(random.randint(1460000000000, 1660000000000))

        mm = t + f
        ml = n['ctype']
        fs = n['fs']
        sp = n['sphdcdn'] if ('sphdcdn' in n.keys()) else 'al_7-tx_3-js_3-ws_7-bd_2-hw_2'
        spp = n['sphdDC'] if ('sphdDC' in n.keys()) else 'huya'
        spd = n['sphd'] if ('sphd' in n.keys()) else '264_*-265_'
        ll = mm + '|' + ml + '|103'
        ms = hashlib.md5(ll.encode("utf-8")).hexdigest()
        h = '_'.join([p, t, s, ms, l])
        m = hashlib.md5(h.encode('utf-8')).hexdigest()
        urls = "{}?wsSecret={}&wsTime={}&seqid={}&ctype={}&ver=1&txyp={}&fs={}&&sphdcdn={}&sphdDC={}&sphd={}&t=103&ratio=4000&u={}&t=103&sv=2110211124".format(i, m, l, mm, ml, mt, fs, sp, spp, spd, t)
        aa, ab = urls.split('//')
        url = 'https://' + ab

        return url
    except Exception as e:
        return ''


def get_real_url(room_id):
    room_url = 'https://mp.huya.com/cache.php?m=Live&do=profileRoom&roomid=' + str(room_id)

    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.100 Mobile Safari/537.36 '
    }
    data = requests.get(url=room_url, headers=header).json()

    multiLine = data['data']['stream']['flv']['multiLine']
    # print(multiLine)
    urls = {}
    liveData = data['data']['liveData']

    urls['name'] = liveData['nick'] + '-' + liveData['introduction'].replace('"', '')
    for i in range(len(multiLine)):
        obj = multiLine[i]
        if obj['url'] is not None:
            liveline = live(obj['url'])
            urls['url' + str(i + 1)] = liveline
    return urls


if __name__ == '__main__':
    try:
        try:
            r = sys.argv[1]
        except:
            r = input('请输入虎牙直播房间号：\n')
        print(get_real_url(r))
    except Exception as e:
        print(e)