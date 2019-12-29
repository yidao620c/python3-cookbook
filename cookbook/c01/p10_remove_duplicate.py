#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 消除序列重复值并保持顺序
Desc : 
"""


def dedupe(items):
    """元素都是hashable"""
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


def dedupe2(items, key=None):
    """元素不是hashable的时候"""
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def remove_dup():
    a = [1, 5, 2, 1, 9, 1, 5, 10]
    print(list(dedupe(a)))

    a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
    print(list(dedupe2(a, key=lambda d: (d['x'], d['y']))))
    print(list(dedupe2(a, key=lambda d: d['x'])))


if __name__ == '__main__':
    remove_dup()
