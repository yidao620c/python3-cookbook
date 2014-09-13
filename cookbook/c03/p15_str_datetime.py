#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字符串转换为datetime
Desc : 
"""
from datetime import datetime


def str_datetime():
    text = '2012-09-20'
    y = datetime.strptime(text, '%Y-%m-%d')
    z = datetime.now()
    diff = z - y
    print(diff)

    print(z)
    nice_z = datetime.strftime(z, '%A %B %d, %Y')
    print(nice_z)


def parse_ymd(s):
    '''自定义解析，要快很多'''
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


if __name__ == '__main__':
    str_datetime()

