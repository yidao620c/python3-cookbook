#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 精确的浮点数运算
Desc : 
"""
from decimal import Decimal



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



if __name__ == '__main__':
    acc_deciamal()
