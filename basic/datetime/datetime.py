#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
import datetime
__author__ = 'Xiong Neng'


def my_datetime():
    today = datetime.datetime.now()
    print(today.ctime())

    oneday = datetime.timedelta(days=1)
    tomorrow = today + oneday
    print(tomorrow.ctime())

if __name__ == '__main__':
    my_datetime()
