#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""
from collections import Iterable


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


def flatten_seq():
    items = [1, 2, [3, 4, [5, 6], 7], 8]
    # Produces 1 2 3 4 5 6 7 8
    for x in flatten(items):
        print(x)
    items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
    for x in flatten(items):
        print(x)

if __name__ == '__main__':
    flatten_seq()