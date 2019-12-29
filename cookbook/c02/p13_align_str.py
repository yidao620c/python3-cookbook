#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 对齐字符串
Desc : 
"""


def align_str():
    text = 'Hello World'
    print(text.ljust(20))
    print(text.rjust(20))
    print(text.center(20))

    # 填充字符
    print(text.rjust(20,'='))
    print(text.center(20,'*'))

    # format函数
    print(format(text, '>20'))
    print(format(text, '<20'))
    print(format(text, '^20'))
    # 同时增加填充字符
    print(format(text, '=>20s'))
    print(format(text, '*^20s'))

    # 格式化多个值
    print('{:=>10s} {:*^10s}'.format('Hello', 'World'))

    # 格式化数字
    x = 1.2345
    print(format(x, '=^10.2f'))


if __name__ == '__main__':
    align_str()

