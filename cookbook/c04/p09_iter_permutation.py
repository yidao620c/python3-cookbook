#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 排列组合迭代
Desc : 
"""
from itertools import permutations
from itertools import combinations
from itertools import combinations_with_replacement


def iter_permutation():
    """排列组合"""

    items = ['a', 'b', 'c']

    # 全排列
    for p in permutations(items):
        print(p)

    # 指定长度
    for p in permutations(items, 2):
        print(p)

    # 组合
    for c in combinations(items, 3):
        print(c)

    # 可重复组合
    for c in combinations_with_replacement(items, 3):
        print(c)

if __name__ == '__main__':
    iter_permutation()
