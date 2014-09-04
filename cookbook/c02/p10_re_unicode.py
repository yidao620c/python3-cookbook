#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 在正则式中使用Unicode
Desc : 
"""
import re


def re_unicode():
    num = re.compile('\d+')

    # ASCII digits
    print(num.match('123'))

    # 阿拉伯数字
    print(num.match('\u0661\u0662\u0663'))

    # 匹配所有阿拉伯编码字符
    arabic = re.compile('[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+')

    # 大小写忽略情形
    pat = re.compile('stra\u00dfe', re.IGNORECASE)
    s = 'straße'
    print(pat.match(s))
    print(pat.match(s.upper()))  # Doesn't match
    print(s.upper())  # 大小写转换


if __name__ == '__main__':
    re_unicode()

