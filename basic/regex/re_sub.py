#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 正则式分组替换示例
"""
import re


class Nth(object):
    """
    如果 sub 函数的第二个参数是个函数，则每次匹配到的时候都会执行这个函数。
    函数接受匹配到的那个 match object 作为参数，返回用来替换的字符串。
    利用这个特性就可以只在第 N 次匹配的时候返回要替换成的字符串，其他时候原样返回不做替换即可。
    """
    def __init__(self, nth, replacement):
        self.nth = nth
        self.replacement = replacement
        self.calls = 0

    def __call__(self, matchobj):
        self.calls += 1
        if self.calls == self.nth:
            return self.replacement
        return matchobj.group(0)


def re_sub():
    a = re.sub(r'(foo)(bar)', r'\g<1>123\g<2>', 'foobar')
    print(a)

    a = re.sub('a', 'A', 'abcasd')  # 找到a用A替换，后面见和group的配合使用
    pat = re.compile('a')
    b = pat.sub('A', 'abcasd')
    print(b)

    # 通过组进行更新替换：
    pat = re.compile(r'(www\.)(.*)(\..{3})')  # 正则表达式
    print(pat.match('www.dxy.com').group(2))
    # 通过正则匹配找到符合规则的”www.dxy.com“ ，取得组2字符串，用baidu替换之
    print('-----------')
    print(pat.sub(r'\g<1>baidu\g<3>', 'hello,www.dxy.com'))

    pat = re.compile(r'(\w+) (\w+)')
    s = 'hello world ! hello hz !'
    pat.findall('hello world ! hello hz !')
    # [('hello', 'world'), ('hello', 'hz')]
    # 通过正则得到组1(hello)，组2(world)，再通过sub去替换。即组1替换组2，组2替换组1，调换位置。
    print(pat.sub(r'\2 \1', s))

    # 替换字符串中第3个出现的good
    pat = re.compile(r'(good)')
    a = pat.sub(Nth(3, 'bad'), 'This is a good story, good is good. Oh, good')
    print(a)
    # 传入一个lambda函数，在匹配处两边加双引号
    a = pat.sub(lambda mo: '"' + mo.group(0) + '"', 'This is a good story, good is ')
    print(a)


if __name__ == '__main__':
    re_sub()

