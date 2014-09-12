#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""
import cmath


def complex_math():
    a = complex(2, 4)
    b = 3 - 5j
    print(a.conjugate())

    # 正弦 余弦 平方根等
    print(cmath.sin(a))
    print(cmath.cos(a))
    print(cmath.sqrt(a))



if __name__ == '__main__':
    complex_math()
