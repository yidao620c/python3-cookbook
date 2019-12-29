#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 精确的浮点数运算
Desc : 
"""
from decimal import Decimal
from decimal import localcontext
import math


def acc_deciamal():
    a = 4.2
    b = 2.1
    print(a + b)
    print((a + b) == 6.3)

    # 使用decimal模块
    a = Decimal('4.2')
    b = Decimal('2.1')
    print(a + b)
    print((a + b) == Decimal('6.3'))

    a = Decimal('1.3')
    b = Decimal('1.7')
    print(a / b)
    with localcontext() as ctx:
        ctx.prec = 3
        print(a / b)

    nums = [1.23e+18, 1, -1.23e+18]
    print(sum(nums))
    print(math.fsum(nums))


if __name__ == '__main__':
    acc_deciamal()
