# 将浮点数n的小数点后p位舍入到0或5
import math
from decimal import Decimal


def round_5(n, p):
    # 将小数点后p位变成整数进行处理（注意：可能会因为放大而导致溢出错误，这里没有考虑此情况的处理）
    i = int(round(n, p) * (10 ** p))
    # 获取 i 的末位
    last_digit = i % (10 ** (p - 1))
    # 末位为 0/1/2，截取为0
    # 末位为 3/4/5/6, 截取为5
    # 末位为 7/8/9，进位为10
    if (last_digit >= 0 and last_digit <= 2):
        result = i // 10 * 10
    elif (last_digit >= 3 and last_digit <= 6):
        result = i // 10 * 10 + 5
    else:
        result = ((i // 10) + 1) * 10

    return result / (10 ** p)


# 将浮点数n的小数点后p位舍入到0或5
def round_4(n, p):
    # 将小数点后p位变成整数进行处理（注意：可能会因为放大而导致溢出错误，这里没有考虑此情况的处理）
    i = int(round(n, p) * (10 ** p))
    # 获取 i 的末位
    last_digit = i % (100 ** (p - 1))
    # 末位为 0/1/2，截取为0
    # 末位为 3/4/5/6, 截取为5
    # 末位为 7/8/9，进位为10
    if 10 <= last_digit <= 12:
        result = i // 10 * 10
    elif 13 <= last_digit <= 16:
        result = i // 10 * 10 + 5
    else:
        result = ((i // 10) + 1) * 10

    return result / (10 ** p)


def myround(x, base=5):
    return base * round(x / base)


def myround2(x, prec=2, base=.05):
    return round(base * round(float(x) / base), prec)


# def my_round(x, prec=2, base=0.2):
#     return (base * (np.array(x) / base).round()).round(prec)


if __name__ == "__main__":
    print("%.2f" % round_5(3037.73, 2))  # 3037.75

    print("%.2f" % round_4(3037.13, 2))  # 3037.75
    print("%.2f" % round_5(3037.72, 2))  # 3037.70
    print("%.2f" % round_5(3037.78, 2))  # 3037.80

    print(myround2(3037.78, 2, 0.5))

    # 针对小数进位
    from _pydecimal import Decimal, Context, ROUND_HALF_UP
    print(Context(prec=1, rounding=ROUND_HALF_UP).create_decimal('0.1'))

    f_num = math.ceil(0.1)
    print(f_num)

