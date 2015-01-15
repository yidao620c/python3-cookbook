#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 简单的正则式搜索，包括分组捕获
    Desc : 正则式例子
     建议阅读Jeffrey E. F. Friedl编写的《精通正则表达式》
    （Mastering Regular Expression）
"""
import re

__author__ = 'Xiong Neng'


def my_re():
    # group示例
    data = 'Thu'
    patt1 = r'^(\w{3})'
    m = re.match(patt1, data)
    print(m.group(1))
    patt2 = r'^(\w){3}'
    m = re.match(patt2, data)
    print(m.group(1))

    # 贪婪匹配
    data = "Sat Mar 21 09:20:57 2009::spiepu@ovwdmrnuw.com::1237598457-6-9"
    # 获取最后的那三个连字符连起来的三个数，
    # 搜索比匹配更合适，因为不在开头
    patt = r'\d+-\d+-\d+'
    print(re.search(patt, data).group())  # 打印出  1237598457-6-9
    # 使用匹配，必须用到group
    patt = r'.+(\d+-\d+-\d+)'
    print(re.match(patt, data).group(1))  # 打印出  7-6-9，知道贪婪的厉害了吧。哈哈
    # 接下来使用非贪婪操作符?
    patt = r'.+?(\d+-\d+-\d+)'
    print(re.match(patt, data).group(1))  # 打印出  1237598457-6-9
    # 只获取三个数的中间那个数字：
    patt = r'-(\d+)-'
    print(re.search(patt, data).group())   # 打印-6-
    print(re.search(patt, data).group(1))  # 打印6


def my_pattern():
    # (?ims) i表示忽略大小写，m表示多行模式，s表示.可以匹配所有字符，包括换行符
    s = "This is a book, And Hello World!! Hello you World?"
    print(1, re.match(r'.*Hello', s).group())
    # 匹配圆括号中的正则式，但丢弃匹配的子字符串
    print(2, re.match(r'.*(?:Hello)', s).group())
    # 分组名为haha
    print(3, re.match(r'.*(?P<haha>Hello)', s).group())
    # 注释，括号中内容被忽略
    print(4, re.match(r'.*(?#Hello)', s).group())
    # 只有在括号中的模式匹配时，才匹配前面的表达式
    print(5, re.match(r'.*Hello (?=World)', s).group())
    # 只有在括号中的模式不匹配时，才匹配前面的表达式
    print(6, re.match(r'.*Hello (?!World)', s).group())
    # 只有在括号中的模式匹配时，才匹配后面的表达式
    print(7, re.match(r'.*(?<=Hello )World', s).group())
    # 只有在括号中的模式不匹配时，才匹配后面的表达式
    print(8, re.match(r'.*(?<!Hello )World', s).group())
    # (?(id|name)ypat|npat) 检查id或name组是否存在，如果存在匹配ypat，否则npat
    print(9, re.match(r'.*(Hello )?(?(1)World|Howdy)', s).group())
    print(9.1, re.search(r'(Hello )?(?(1)World|Howdy)', s).group())


def my_sample():
    """一个详细的字符串搜索、提取、替换示例"""
    text = "Guido will be out of the office from 12/15/2012 - 1/3/2013"

    # 日期的正则式
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

    # 找到并打印所有日期
    for m in datepat.finditer(text):
        print(m.group())

    # z找到所有日期，但是以不同格式打印
    monthnames = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May',
                  'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for m in datepat.finditer(text):
        print("%s %s, %s" % (monthnames[int(m.group(1))], m.group(2), m.group(3)))

    # 将所有日期替换为欧洲日期格式(日/月/年)
    def fix_date(m):
        return "%s/%s/%s" % (m.group(2), m.group(1), m.group(3))
    newtext = datepat.sub(fix_date, text)
    print(newtext)


if __name__ == '__main__':
    my_sample()
