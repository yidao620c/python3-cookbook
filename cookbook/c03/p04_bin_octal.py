#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 不同进制的数字表示输出
Desc : 
"""


def bin_octal():
    x = 1234
    print(type(bin(x)))
    print(bin(x), oct(x), hex(x))

    # format() function
    print(format(x, 'b'))
    print(format(x, 'o'))
    print(format(x, 'x'))

    print(int('4d2', 16))
    print(int('10011010010', 2))


if __name__ == '__main__':
    bin_octal()
