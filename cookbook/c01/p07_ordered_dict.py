#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 排序字典
Desc : 
"""

from collections import OrderedDict

def ordered_dict():
    d = OrderedDict()
    d['foo'] = 1
    d['bar'] = 2
    d['spam'] = 3
    d['grok'] = 4
    # Outputs "foo 1", "bar 2", "spam 3", "grok 4"
    for key in d:
        print(key, d[key])

