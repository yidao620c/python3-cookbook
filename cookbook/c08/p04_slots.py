#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 使用slots来减少内存占用
Desc : 
"""


class Date:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

