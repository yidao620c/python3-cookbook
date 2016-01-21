#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 素数生成
Desc : 埃氏筛法算法
"""


def _odd_iter():
    '''构造以3开始的奇数序列'''
    n = 1
    while True:
        n += 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2

    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)

for n in primes():
    if n < 1000:
        print(n, end=' ')
    else:
        break


