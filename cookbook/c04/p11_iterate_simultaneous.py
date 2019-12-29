#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 同时迭代多个序列
Desc : 
"""
from itertools import zip_longest


def iterate_simul():
    xpts = [1, 5, 4, 2, 10, 7]
    ypts = [101, 78, 37, 15, 62, 99]
    for x, y in zip(xpts, ypts):
        print(x, y)

    a = [1, 2, 3]
    b = ['w', 'x', 'y', 'z']
    for i in zip(a,b):
        print(i)  # 默认是按最短长度
    for i in zip_longest(a,b):
        print(i)
    for i in zip_longest(a, b, fillvalue=0):
        print(i)

    headers = ['name', 'shares', 'price']
    values = ['ACME', 100, 490.1]
    s = dict(zip(headers,values))

    for name, val in zip(headers, values):
        print(name, '=', val)


if __name__ == '__main__':
    iterate_simul()

