#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 日期时区和本地化
Desc : 
"""
from datetime import datetime, timedelta
from pytz import timezone
import pytz


def tz_local():
    d = datetime(2012, 12, 21, 9, 30, 0)
    print(d)

    # Localize the date for Chicago
    central = timezone('US/Central')
    loc_d = central.localize(d)
    print(loc_d)

    # Convert to Bangalore time
    bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
    print(bang_d)


    # 夏令时
    d = datetime(2013, 3, 10, 1, 45)
    loc_d = central.localize(d)
    print(loc_d)
    later = loc_d + timedelta(minutes=30)
    print(later)
    # 使用normalize修正这个问题
    later = central.normalize(loc_d + timedelta(minutes=30))
    print(later)

    # 一个普遍策略是先转换为UTC时间，使用UTC时间来进行计算
    print(loc_d)
    utc_d = loc_d.astimezone(pytz.utc)
    print(utc_d)

    later_utc = utc_d + timedelta(minutes=30)
    # 转回到本地时间
    print(later_utc.astimezone(central))

    # 根据ISO 3166国家代码查找时区名称
    print(pytz.country_timezones['IN'])

if __name__ == '__main__':
    tz_local()

