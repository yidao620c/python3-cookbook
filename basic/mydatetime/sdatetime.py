#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
from datetime import datetime, date, time, timedelta


def my_datetime():
    today = datetime.now()
    print(today.ctime())

    oneday = timedelta(days=1)
    tomorrow = today + oneday
    print(tomorrow.ctime())

    # str to date
    dt = datetime.strptime('2012-01-12 12:12:12', '%Y-%m-%d %H:%M:%S')
    # date to str
    print(dt.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    my_datetime()
