#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 合并多个字典或映射
Desc : 
"""

from collections import ChainMap


def combine_map():
    a = {'x': 1, 'z': 3 }
    b = {'y': 2, 'z': 4 }
    c = ChainMap(a,b)
    print(c['x']) # Outputs 1 (from a)
    print(c['y']) # Outputs 2 (from b)
    print(c['z']) # Outputs 3 (from a)

    print(len(c))
    print(list(c.keys()))
    print(list(c.values()))

    c['z'] = 10
    c['w'] = 40
    del c['x']
    print(a)
    # del c['y']

    values = ChainMap()
    values['x'] = 1
    # Add a new mapping
    values = values.new_child()
    values['x'] = 2
    # Add a new mapping
    values = values.new_child()
    values['x'] = 3
    print(values)
    print(values['x'])
    # Discard last mapping
    values = values.parents
    print(values['x'])
    # Discard last mapping
    values = values.parents
    print(values['x'])
    print(values)


if __name__ == '__main__':
    combine_map()