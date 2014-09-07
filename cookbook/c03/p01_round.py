#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 四舍五入运算
Desc : 
"""


def round_num():
    print(round(1.23, 1))
    print(round(1.27, 1))
    print(round(-1.27, 1))
    print(round(1.25361,3))

    # 舍入数为负数
    a = 1627731
    print(round(a, -1))
    print(round(a, -2))
    print(round(a, -3))

    # 格式化输出
    x = 1.23456
    print(format(x, '0.2f'))
    print(format(x, '0.3f'))
    print('value is {:0.3f}'.format(x))

    # 不要自以为是的用round去修正一些精度问题
    a = 2.1
    b = 4.2
    c = a + b
    print(c)
    c = round(c, 2)  # "Fix" result (???)
    print(c)

if __name__ == '__main__':
    round_num()

