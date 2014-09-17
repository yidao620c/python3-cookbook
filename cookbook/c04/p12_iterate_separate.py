#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 在不同容器中迭代
Desc : 
"""
from itertools import chain


def iter_separate():
    a = [1, 2, 3, 4]
    b = ['x', 'y', 'z']
    for x in chain(a, b):
        print(x)

if __name__ == '__main__':
    iter_separate()

