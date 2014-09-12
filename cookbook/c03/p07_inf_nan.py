#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 无穷大与NaN
Desc : 
"""


def inf_nan():
    a = float('inf')
    b = float('-inf')
    c = float('nan')

    print(a + 45)
    print(a + 45 == a)
    print(a * 10 == a)
    print(10 / a)

    # undifined
    print(a / a)
    print(a + b)

    print(c + 23)
    print(c / 2 == c)  # False ?


if __name__ == '__main__':
    inf_nan()

