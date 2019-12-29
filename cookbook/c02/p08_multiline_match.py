#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 多行匹配
Desc : 
"""
import re


def multiline_match():
    comment = re.compile(r'/\*(.*?)\*/')
    text1 = '/* this is a comment */'
    text2 = '''/* this is a
    multiline comment */
    '''
    print(comment.findall(text1))
    print(comment.findall(text2))

    # 修正模式
    comment = re.compile(r'/\*((?:.|\n)*?)\*/')
    print(comment.findall(text2))

    # 使用标志参数re.DOTALL，复杂匹配时不推荐
    comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
    print(comment.findall(text2))


if __name__ == '__main__':
    multiline_match()
