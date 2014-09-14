#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 最后的周五
Desc : 
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']


def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date


def last_friday():
    print(datetime.today())
    print(get_previous_byday('Monday'))
    print(get_previous_byday('Tuesday'))
    print(get_previous_byday('Friday'))
    print(get_previous_byday('Saturday'))
    # 显式的传递开始日期
    print(get_previous_byday('Sunday', datetime(2012, 12, 21)))

    # 使用dateutil模块
    d = datetime.now()
    # 下一个周五
    print(d + relativedelta(weekday=FR))
    # 上一个周五
    print(d + relativedelta(weekday=FR(-1)))
    # 下一个周六， 为什么如果今天是周六，下一个/上一个都返回今天的日期？？
    print(d + relativedelta(weekday=SA))
    # 上一个周六
    print(d + relativedelta(weekday=SA(-1)))


if __name__ == '__main__':
    last_friday()


