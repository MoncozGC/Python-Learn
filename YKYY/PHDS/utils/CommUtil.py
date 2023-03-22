# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/1/25 11:04
# Desc  : 工具类
import logging
from logging import handlers


def getNowTimeStr():
    import datetime
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def print_ts(*args):
    # tuple = ("【%s】" % getNowTimeStr(),) + args
    # print(*tuple)
    get_logger(*args)


def get_logger(*args):
    LOG_FILE = r'./book_tool.txt'

    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
    fmt = '%(asctime)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger('book_tool')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    tuple = ("【%s】" % getNowTimeStr(),) + args
    logger.info(args)
    return print(*tuple)


def print_format(format_str, *args):
    if len(args) > 0:
        print_ts(format_str % args)
    else:
        print_ts(format_str)


def decimalRound(value, digit=4):
    """
    decimal 四舍五入
    """
    if value is None or str(value) == '':
        raise ValueError(' decimalRound value is '' or None ')
    import decimal
    from decimal import Decimal
    # 修改decimal默认使用的精确度值方法(趋向0取整)
    decimal.getcontext().rounding = "ROUND_HALF_UP"
    _digit = '0.' + '0' * digit if digit > 0 else '0'
    return Decimal(str(value)).quantize(Decimal(_digit))


def roundStr(value, digit=4):
    format = '%.' + str(digit) + 'f'
    return format % decimalRound(value, digit)


def _mdiv(a, b):
    try:
        from decimal import Decimal
        return float(Decimal(str(a)) / Decimal(str(b)))
    except:
        pass
    return 0


def _multipli(a, b):
    try:
        from decimal import Decimal
        return float(Decimal(str(a)) * Decimal(str(b)))
    except:
        pass
    return 0


def _mdiv_round(a, b, digit=4):
    return decimalRound(_mdiv(a, b), digit)


def _multipli_round(a, b, digit=4):
    return decimalRound(_multipli(a, b), digit)


def _mdiv_round_f(a, b, digit=4):
    return float(decimalRound(_mdiv(a, b), digit))


def _multipli_round_f(a, b, digit=4):
    return float(decimalRound(_multipli(a, b), digit))


if __name__ == '__main__':
    a = 2
    b = 4.5
    print(_multipli_round(a, b))
