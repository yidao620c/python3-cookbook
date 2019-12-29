#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义类的多个构造函数
Desc : 
"""

import time


class Date:
    """方法一：使用类方法"""
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

a = Date(2012, 12, 21) # Primary
b = Date.today() # Alternate

