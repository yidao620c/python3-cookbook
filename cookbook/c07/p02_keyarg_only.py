#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 只允许关键字形式的参数
Desc : 
"""


def recv(maxsize, *, block):
    'Receives a message'
    pass

# recv(1024, True) # TypeError
recv(1024, block=True)  # Ok


def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m


minimum(1, 5, 2, -5, 10)  # Returns -5
minimum(1, 5, 2, -5, 10, clip=0)  # Returns 0