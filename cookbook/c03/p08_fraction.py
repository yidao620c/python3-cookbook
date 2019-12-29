#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 分数运算
Desc : 
"""
from fractions import Fraction


def frac():
    a = Fraction(5, 4)
    b = Fraction(7, 16)
    print(print(a + b))
    print(a.numerator, a.denominator)

    c = a + b
    print(float(c))
    print(type(c.limit_denominator(8)))
    print(c.limit_denominator(8))


if __name__ == '__main__':
    frac()
