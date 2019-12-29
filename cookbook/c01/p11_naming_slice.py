#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 命名切片
Desc : 
"""


def name_slice():
    record = '....................100 .......513.25 ..........'
    cost = int(record[20:23]) * float(record[31:37])

    SHARES = slice(20, 23)
    PRICE = slice(31, 37)
    cost = int(record[SHARES]) * float(record[PRICE])
    print(cost)
    print(SHARES.start)
    print(SHARES.stop)
    print(SHARES.step)

    a = slice(5, 50, 2)
    s = 'HelloWorld'
    print(a.indices(len(s)))
    for i in range(*a.indices(len(s))):
        print(s[i])


if __name__ == '__main__':
    name_slice()