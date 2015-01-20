#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
from datetime import datetime, date, time, timedelta


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_millis(dt):
    return '{:.0f}'.format(unix_time(dt) * 1000.0)


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
    tt = datetime(2014, 12, 31, 12, 42, 50)
    print(unix_time_millis(tt))
    # tt = datetime(2015, 10, 12)
    # print(unix_time_millis(tt))

