#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 迭代器和生成器切片
Desc : 
"""
import itertools


def count(n):
    while True:
        yield n
        n += 1


def iter_slice():
    c = count(0)
    for x in itertools.islice(c, 10, 20):
        print(x)


if __name__ == '__main__':
    iter_slice()


