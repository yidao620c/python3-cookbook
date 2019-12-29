#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 函数默认参数
Desc : 
"""

def spam(a, b=42):
    print(a, b)

spam(1) # Ok. a=1, b=42
spam(1, 2) # Ok. a=1, b=2

_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

