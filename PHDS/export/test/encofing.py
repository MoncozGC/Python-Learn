# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/26 21:53
# Desc  : 编码测试

# 说明：UTF兼容ISO8859-1和ASCII，GB18030兼容GBK，GBK兼容GB2312，GB2312兼容ASCII
CODES = ['UTF-8', 'GB18030', 'BIG5', 'cp936']
# UTF-8 BOM前缀字节
UTF_8_BOM = b'\xef\xbb\xbf'


def file_encoding(file_path: str):
    """
    获取文件编码类型

    :param file_path: 文件路径
    :return:
    """
    with open(file_path, 'rb') as f:
        return string_encoding(f.read())


def string_encoding(data: bytes):
    """
    获取字符编码类型

    :param data: 字节数据
    :return:
    """
    # 遍历编码类型
    for code in CODES:
        try:
            data.decode(encoding=code)
            if 'UTF-8' == code and data.startswith(UTF_8_BOM):
                return 'UTF-8-SIG'
            return code
        except UnicodeDecodeError:
            continue
    return 'unknown'


if __name__ == '__main__':
    data = b'¸à¼Á'
    print(string_encoding(data))
