# Author: MoncozGC
# Date  : 2021/12/13 10:49
# Desc  :
# encoding: utf-8

def get_oid(BV_CODE: str):
    # bv = BV_CODE[2:] if "BV" == BV_CODE[:2] else print(BV_CODE)
    print(BV_CODE[:2])


def _multipli(a, b):
    try:
        from decimal import Decimal
        return float(Decimal(str(a)) * Decimal(str(b)))
    except:
        pass
    return 0


def decimalRound(value, digit=4):
    """
    dicimal 四舍五入
    :param value:
    :param digit:
    :return:
    """
    if value is None or str(value) == '':
        raise ValueError(' decimalRound value is '' or None ')
    import decimal
    from decimal import Decimal
    decimal.getcontext().rounding = "ROUND_HALF_UP"
    _digit = '0.' + '0' * digit if digit > 0 else '0'
    return Decimal(str(value)).quantize(Decimal(_digit))


if __name__ == '__main__':
    # get_oid('BV1FL411E7g3')
    print(_multipli(0.0, 0.2))
    print(float(decimalRound(_multipli(0.0, 0.2), 4)))
