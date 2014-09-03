#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字符串搜索和替换
Desc : 
"""
import re
from calendar import month_abbr


def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))


def search_replace():
    text = 'yeah, but no, but yeah, but no, but yeah'
    print(text.replace('yeah', 'yep'))

    # 复杂的模式，使用sub()
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
    print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))

    # 先编译
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    print(datepat.sub(r'\3-\1-\2', text))

    # 更复杂的替换，使用回调函数
    print(datepat.sub(change_date, text))

    # 同时返回替换次数
    newtext, n = datepat.subn(r'\3-\1-\2', text)
    print(newtext, n)


if __name__ == '__main__':
    search_replace()

