#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字符串匹配和搜索
Desc : 
"""
import  re


def match_search():
    # 字面字符串匹配
    text = 'yeah, but no, but yeah, but no, but yeah'
    print(text == 'yeah')
    print(text.startswith('yeah'))
    print(text.endswith('no'))
    print(text.find('no'))

    # 简单的日期匹配
    text1 = '11/27/2012'
    text2 = 'Nov 27, 2012'
    if re.match(r'\d+/\d+/\d+', text1):
        print('yes')
    else:
        print('no')

    if re.match(r'\d+/\d+/\d+', text2):
        print('yes')
    else:
        print('no')

    # 编译模式字符串先
    datepat = re.compile(r'\d+/\d+/\d+')
    if datepat.match(text1):
        print('yes')
    else:
        print('no')

    if datepat.match(text2):
        print('yes')
    else:
        print('no')

    # 使用findall()
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
    print(datepat.findall(text))

    # 括号捕获分组
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    m = datepat.match('11/27/2012')
    print(m.group(0))
    print(m.group(1))
    print(m.group(2))
    print(m.group(3))
    print(m.groups())
    month, day, year = m.groups()
    print(datepat.findall(text))
    for month, day, year in datepat.findall(text):
        print('{}-{}-{}'.format(year, month, day))


    # 迭代方式返回匹配
    for m in datepat.finditer(text):
        print(m.groups())

    # 字符串整个匹配
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
    print(datepat.match('11/27/2012abcdef'))
    print(datepat.match('11/27/2012'))

    # 直接使用re模块级别函数
    print(re.findall(r'(\d+)/(\d+)/(\d+)', text))

if __name__ == '__main__':
    match_search()

